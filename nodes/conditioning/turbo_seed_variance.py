import logging
from contextlib import contextmanager
from dataclasses import dataclass

import node_helpers
import torch


# Based on SeedVarianceEnhancer v2.2 and the Krea 2 adaptation, both MIT-0.
NOISE_INSERT_MODES = [
    "noise on beginning steps",
    "noise on ending steps",
    "noise on all steps",
    "disabled",
]


@dataclass(frozen=True)
class ModeProfile:
    name: str
    padding_eps: float
    use_auto_strength: bool
    auto_strength_scale: float = 1.0
    layer_count: int = 1
    use_reference_krea_noise: bool = False
    std_unbiased: bool = False


MODE_PROFILES = {
    "z-image-turbo": ModeProfile(
        name="z-image-turbo",
        padding_eps=0.0,
        use_auto_strength=True,
        auto_strength_scale=0.1,
    ),
    "krea2-turbo": ModeProfile(
        name="krea2-turbo",
        padding_eps=1e-6,
        use_auto_strength=True,
        use_reference_krea_noise=True,
        std_unbiased=True,
    ),
    "flux2-klein": ModeProfile(
        name="flux2-klein",
        padding_eps=1e-6,
        use_auto_strength=True,
        auto_strength_scale=0.01,
        layer_count=3,
    ),
}


@contextmanager
def preserved_torch_rng():
    cpu_state = torch.get_rng_state()
    cuda_state = torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None
    try:
        yield
    finally:
        torch.set_rng_state(cpu_state)
        if cuda_state is not None:
            torch.cuda.set_rng_state_all(cuda_state)


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def clone_conditioning_item(item):
    tensor = item[0]
    metadata = item[1].copy() if len(item) > 1 and isinstance(item[1], dict) else {}
    return [tensor, metadata]


class TurboSeedVariance:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning": ("CONDITIONING",),
                "mode": (
                    list(MODE_PROFILES.keys()),
                    {
                        "default": "z-image-turbo",
                        "tooltip": "Use z-image-turbo for Z-Image Turbo, krea2-turbo for Krea 2 Turbo, or flux2-klein for Flux2 Klein distilled workflows.",
                    },
                ),
                "randomize_percent": (
                    "FLOAT",
                    {
                        "default": 50.0,
                        "min": 1.0,
                        "max": 100.0,
                        "step": 1.0,
                        "tooltip": "Percentage of embedding values that receive noise.",
                    },
                ),
                "auto_strength_factor": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 0.0,
                        "max": 100.0,
                        "step": 0.05,
                        "tooltip": "If greater than 0, noise scale is measured embedding std times this factor and the selected mode profile. Set to 0 to use strength.",
                    },
                ),
                "strength": (
                    "FLOAT",
                    {
                        "default": 20.0,
                        "min": 0.0,
                        "max": 0xFFFFFFFF,
                        "step": 0.00001,
                        "tooltip": "Absolute fallback noise scale used when auto_strength_factor is 0.",
                    },
                ),
                "noise_insert": (
                    NOISE_INSERT_MODES,
                    {
                        "default": "noise on beginning steps",
                        "tooltip": "Where the noised conditioning is active during generation.",
                    },
                ),
                "steps_switchover_percent": (
                    "FLOAT",
                    {
                        "default": 25.0,
                        "min": 1.0,
                        "max": 99.0,
                        "step": 1.0,
                        "tooltip": "Percent of sampling steps before switching between noised and clean conditioning. Try 20 for z-image-turbo, 25 for krea2-turbo 8-step workflows.",
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "control_after_generate": True,
                        "tooltip": "Seed used to choose noised embedding values and noise amounts.",
                    },
                ),
                "mask_starts_at": (
                    ["beginning", "end"],
                    {"tooltip": "Which end of the prompt is protected from noise."},
                ),
                "mask_percent": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": 0.0,
                        "max": 99.0,
                        "step": 1.0,
                        "tooltip": "Percentage of prompt tokens protected from noise.",
                    },
                ),
                "log_to_console": (
                    "BOOLEAN",
                    {
                        "default": False,
                        "tooltip": "Print embedding statistics and effective noise information to the ComfyUI console.",
                    },
                ),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("conditioning",)
    FUNCTION = "randomize_conditioning"
    CATEGORY = "geocine/conditioning"
    DESCRIPTION = "Add seed-dependent noise to text conditioning to increase variation for turbo/distilled low-step models."
    SEARCH_ALIASES = [
        "seed variance",
        "seedvarianceenhancer",
        "turbo seed variance",
        "z-image",
        "z-image turbo",
        "z-image-turbo",
        "krea2",
        "krea2 turbo",
        "krea2-turbo",
        "flux2",
        "klein",
        "conditioning noise",
    ]

    def _attention_mask(self, metadata, tensor):
        attention_mask = metadata.get("attention_mask")
        if not isinstance(attention_mask, torch.Tensor):
            return None

        if attention_mask.dim() == 1:
            attention_mask = attention_mask.unsqueeze(0)
        elif attention_mask.dim() > 2:
            attention_mask = attention_mask.reshape(attention_mask.shape[0], -1)

        if attention_mask.shape[-1] != tensor.size(1):
            return None

        attention_mask = attention_mask.to(device=tensor.device, dtype=torch.bool)
        if attention_mask.shape[0] == 1 and tensor.size(0) > 1:
            attention_mask = attention_mask.expand(tensor.size(0), -1)
        if attention_mask.shape[0] != tensor.size(0):
            return None

        return attention_mask

    def _token_activity(self, tensor, eps, attention_mask=None):
        if attention_mask is not None:
            return attention_mask.any(dim=0).tolist()

        if eps > 0:
            return [not torch.all(tensor[:, index, ...].abs() < eps).item() for index in range(tensor.size(1))]
        return [not torch.all(tensor[:, index, ...] == 0).item() for index in range(tensor.size(1))]

    def _real_region(self, tensor, eps, attention_mask=None):
        token_activity = self._token_activity(tensor, eps, attention_mask)
        last_real = -1
        for index, is_real in enumerate(token_activity):
            if is_real:
                last_real = index

        if last_real >= 0 and last_real < tensor.size(1) - 1:
            real_slice = slice(0, last_real + 1)
            return real_slice, last_real + 1, token_activity

        return slice(0, tensor.size(1)), tensor.size(1), token_activity

    def _select_conditioning_items(self, conditioning, noise_insert):
        if len(conditioning) == 1:
            selected = clone_conditioning_item(conditioning[0])
            return selected, clone_conditioning_item(conditioning[0])

        if noise_insert == "noise on beginning steps":
            return clone_conditioning_item(conditioning[0]), clone_conditioning_item(conditioning[1])

        if noise_insert == "noise on ending steps":
            return clone_conditioning_item(conditioning[1]), clone_conditioning_item(conditioning[0])

        first = clone_conditioning_item(conditioning[0])
        second = clone_conditioning_item(conditioning[1])
        if first[1].get("SVH_tag") != "noisy" and second[1].get("SVH_tag") == "noisy":
            return second, clone_conditioning_item(conditioning[1])
        return first, clone_conditioning_item(conditioning[0])

    def _effective_strength(self, profile, tensor, real_slice, auto_strength_factor, strength):
        real_region = tensor[:, real_slice, :]
        measured_std = real_region.std(unbiased=profile.std_unbiased).item()
        if profile.use_auto_strength and auto_strength_factor > 0:
            return measured_std * auto_strength_factor * profile.auto_strength_scale, measured_std
        return strength, measured_std

    def _noise_shape(self, tensor, profile):
        if profile.layer_count <= 1 or tensor.size(-1) % profile.layer_count != 0:
            return tensor.shape
        return (*tensor.shape[:-1], 1, tensor.size(-1) // profile.layer_count)

    def _expand_layer_coherent(self, value, tensor, profile):
        if value.shape == tensor.shape:
            return value
        value = value.expand(*tensor.shape[:-1], profile.layer_count, value.size(-1))
        return value.reshape_as(tensor)

    def _noise_and_mask(self, tensor, randomize_percent, seed, profile, effective_strength):
        if profile.use_reference_krea_noise:
            with preserved_torch_rng():
                torch.manual_seed(seed)
                noise = torch.rand_like(tensor) * 2 * effective_strength - effective_strength
                torch.manual_seed(seed + 1)
                mask = torch.bernoulli(torch.ones_like(tensor) * randomize_percent).bool()
            return noise, mask

        noise_shape = self._noise_shape(tensor, profile)
        with preserved_torch_rng():
            torch.manual_seed(seed)
            noise = torch.rand(noise_shape, device=tensor.device, dtype=tensor.dtype) * 2 * effective_strength - effective_strength
            torch.manual_seed(seed + 1)
            mask = torch.rand(noise_shape, device=tensor.device, dtype=tensor.dtype) < randomize_percent
        return (
            self._expand_layer_coherent(noise, tensor, profile),
            self._expand_layer_coherent(mask, tensor, profile),
        )

    def _is_conditioning_item(self, item):
        return isinstance(item, (list, tuple)) and len(item) >= 2

    def _apply_prompt_mask(self, noise_mask, tensor, token_activity, real_tokens, mask_starts_at, mask_percent, attention_mask=None):
        protected = torch.zeros((1, tensor.size(1), 1), dtype=torch.bool, device=tensor.device)

        if mask_percent > 0:
            protected_count = int(real_tokens * mask_percent)
            if mask_starts_at == "end":
                start = real_tokens - protected_count
                end = real_tokens
            else:
                start = 0
                end = protected_count
            protected[:, start:end, :] = True

        protected = protected.expand(tensor.size(0), -1, -1).clone()
        if attention_mask is not None:
            protected = protected | ~attention_mask.view(tensor.size(0), tensor.size(1), 1)
        else:
            null_tokens = torch.tensor(
                [not is_real for is_real in token_activity],
                dtype=torch.bool,
                device=tensor.device,
            ).view(1, -1, 1)
            protected = protected | null_tokens

        if protected.any():
            return noise_mask & ~protected.expand_as(noise_mask)
        return noise_mask

    def _log_stats(self, profile, tensor, real_slice, real_tokens, measured_std, effective_strength, noise_mask, modified_noise, seed):
        real_tensor = tensor[:, real_slice, :]
        real_noise = modified_noise[:, real_slice, :]
        noised_percent = noise_mask[:, real_slice, :].float().mean().item() * 100.0
        base_norm = real_tensor.norm().item()
        l2_percent = (real_noise.norm().item() / base_norm * 100.0) if base_norm > 0 else 0.0

        logging.info(
            "TurboSeedVariance[%s]: shape=%s real_tokens=%s/%s std=%.6f effective_strength=%.6f values_noised=%.1f%% l2_perturbation=%.2f%% layer_count=%s seed=%s",
            profile.name,
            tuple(tensor.shape),
            real_tokens,
            tensor.size(1),
            measured_std,
            effective_strength,
            noised_percent,
            l2_percent,
            profile.layer_count,
            seed,
        )

    def randomize_conditioning(
        self,
        conditioning,
        mode,
        randomize_percent,
        auto_strength_factor,
        strength,
        noise_insert,
        steps_switchover_percent,
        seed,
        mask_starts_at,
        mask_percent,
        log_to_console,
    ):
        profile = MODE_PROFILES[mode]
        randomize_percent = clamp(randomize_percent, 1.0, 100.0) / 100.0
        mask_percent = clamp(mask_percent, 0.0, 99.0) / 100.0
        steps_switchover_percent = clamp(steps_switchover_percent, 1.0, 99.0) / 100.0

        if noise_insert == "disabled":
            return (conditioning,)

        if (
            len(conditioning) < 1
            or not self._is_conditioning_item(conditioning[0])
            or (len(conditioning) > 1 and not self._is_conditioning_item(conditioning[1]))
        ):
            if log_to_console:
                logging.warning("TurboSeedVariance received an empty conditioning. Passing it through unchanged.")
            return (conditioning,)

        if len(conditioning) > 2 and log_to_console:
            logging.warning("TurboSeedVariance only uses the first two conditioning entries.")

        noised_item, clean_item = self._select_conditioning_items(conditioning, noise_insert)
        tensor = noised_item[0]
        if not isinstance(tensor, torch.Tensor):
            if log_to_console:
                logging.warning("TurboSeedVariance received conditioning without a tensor. Passing it through unchanged.")
            return (conditioning,)

        attention_mask = self._attention_mask(noised_item[1], tensor)
        real_slice, real_tokens, token_activity = self._real_region(tensor, profile.padding_eps, attention_mask)
        effective_strength, measured_std = self._effective_strength(
            profile,
            tensor,
            real_slice,
            auto_strength_factor,
            strength,
        )

        if effective_strength == 0:
            return (conditioning,)

        modified_noise, noise_mask = self._noise_and_mask(tensor, randomize_percent, seed, profile, effective_strength)
        noise_mask = self._apply_prompt_mask(
            noise_mask,
            tensor,
            token_activity,
            real_tokens,
            mask_starts_at,
            mask_percent,
            attention_mask,
        )

        modified_noise = modified_noise * noise_mask
        noisy_tensor = tensor + modified_noise

        if log_to_console:
            self._log_stats(
                profile,
                tensor,
                real_slice,
                real_tokens,
                measured_std,
                effective_strength,
                noise_mask,
                modified_noise,
                seed,
            )

        noisy_embedding = [[noisy_tensor, noised_item[1]]]
        clean_embedding = [clean_item]

        if noise_insert == "noise on beginning steps":
            conditioning_out = node_helpers.conditioning_set_values(
                noisy_embedding,
                {"start_percent": 0.0, "end_percent": steps_switchover_percent, "SVH_tag": "noisy"},
            )
            conditioning_out += node_helpers.conditioning_set_values(
                clean_embedding,
                {"start_percent": steps_switchover_percent, "end_percent": 1.0},
            )
            return (conditioning_out,)

        if noise_insert == "noise on ending steps":
            conditioning_out = node_helpers.conditioning_set_values(
                clean_embedding,
                {"start_percent": 0.0, "end_percent": steps_switchover_percent},
            )
            conditioning_out += node_helpers.conditioning_set_values(
                noisy_embedding,
                {"start_percent": steps_switchover_percent, "end_percent": 1.0, "SVH_tag": "noisy"},
            )
            return (conditioning_out,)

        noisy_embedding[0][1].pop("start_percent", None)
        noisy_embedding[0][1].pop("end_percent", None)
        return (noisy_embedding,)
