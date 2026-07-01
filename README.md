<p align="center">
  <img src="./assets/header.png" alt="geocine-comfyui node graph header" width="100%" />
</p>

# geocine-comfyui

Small utility nodes for ComfyUI workflows, focused on practical image, text, seed, LLM, and LoRA helpers.

## Nodes

Display names stay readable in ComfyUI. Saved workflow node IDs use a `Geocine` prefix to avoid collisions with other custom nodes.

- `Image Selector` (`GeocineImageSelector`): choose one image from a batch by index.
- `Image Scale` (`GeocineImageScale`): scale an image by width, height, or percentage.
- `Turbo Seed Variance` (`GeocineTurboSeedVariance`): add seed-dependent conditioning noise for turbo/distilled low-step models.
- `Seed to Noise` (`GeocineSeedToNoise`): convert a seed into ComfyUI random noise.
- `LoRA Name List` (`GeocineLoraNameList`): build a list of selected LoRA names.
- `LoRA Loader Stack` (`GeocineLoraLoaderStack`): apply multiple LoRAs to a model in order, without a CLIP input.
- `Prompt Text` (`GeocinePromptText`): pass prompt text through a simple string node.
- `Text Replace` (`GeocineTextReplace`): replace text using string inputs.
- `Show Text` (`GeocineShowTextNode`): display text output inside the workflow.
- `OpenAI Compatible LLM` (`GeocineOpenAICompatibleLLM`): call an OpenAI-compatible chat endpoint.
- `Preview Text` (`GeocinePreviewText`): preview text output with optional JSON formatting.

## Install

Clone this repository into `ComfyUI/custom_nodes`, then restart ComfyUI.

```sh
git clone https://github.com/geocine/geocine-comfyui.git ComfyUI/custom_nodes/geocine-comfyui
```

## Development

Python node implementations live under `nodes/<domain>/`. Frontend extensions live in the mirrored `web/js/<domain>/` folders. The root `__init__.py` only registers stable ComfyUI node IDs, display names, and `WEB_DIRECTORY`.

## Publish

Maintainers can publish a new registry version from a clean checkout:

```sh
./publish
./publish minor
./publish major
```

`./publish` defaults to a patch bump, commits the new `pyproject.toml` version, then runs `python -m comfy node publish`.
