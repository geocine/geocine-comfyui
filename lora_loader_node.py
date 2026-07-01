import folder_paths
from nodes import LoraLoaderModelOnly


class LoraLoaderStack:
    @classmethod
    def INPUT_TYPES(cls):
        loras = ["None"] + folder_paths.get_filename_list("loras")
        return {
            "required": {
                "model": ("MODEL", {"tooltip": "The diffusion model the LoRAs will be applied to."}),
                "lora_name_1": (loras, {"tooltip": "The first LoRA to apply."}),
                "lora_strength_1": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": -100.0,
                        "max": 100.0,
                        "step": 0.01,
                        "tooltip": "How strongly to modify the diffusion model.",
                    },
                ),
            },
            "hidden": {
                "prompt": "PROMPT",
                "id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "load_loras"
    CATEGORY = "geocine/lora"
    DESCRIPTION = "Apply multiple LoRAs to a model in order, without requiring a CLIP input."
    SEARCH_ALIASES = ["lora", "load lora", "lora loader", "lora stack", "model only lora"]

    def __init__(self):
        self.lora_loader = LoraLoaderModelOnly()

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    @staticmethod
    def _prompt_inputs(kwargs):
        prompt = kwargs.get("prompt") or {}
        node_id = kwargs.get("id")
        if prompt and node_id is not None:
            node = prompt.get(node_id) or prompt.get(str(node_id))
            if node:
                return node.get("inputs", {})
        return kwargs

    @staticmethod
    def _as_float(value, default=1.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _iter_loras(self, node_inputs):
        index = 1
        while True:
            name_key = f"lora_name_{index}"
            strength_key = f"lora_strength_{index}"
            if name_key not in node_inputs:
                break

            lora_name = node_inputs.get(name_key)
            strength = self._as_float(node_inputs.get(strength_key, 1.0))
            if lora_name and lora_name != "None" and strength != 0.0:
                yield lora_name, strength

            index += 1

    def load_loras(self, model, **kwargs):
        node_inputs = self._prompt_inputs(kwargs)
        for lora_name, strength in self._iter_loras(node_inputs):
            model = self.lora_loader.load_lora_model_only(model, lora_name, strength)[0]
        return (model,)
