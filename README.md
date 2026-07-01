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

Install from the ComfyUI registry with the Comfy CLI, then restart ComfyUI.

```sh
comfy node install geocine-comfyui
```

In ComfyUI Manager, search for `geocine-comfyui`, click install, then restart ComfyUI.

You can also clone this repository into `ComfyUI/custom_nodes` manually.

```sh
git clone https://github.com/geocine/geocine-comfyui.git ComfyUI/custom_nodes/geocine-comfyui
```

## Development

Development and publishing notes live in [DEVELOPMENT.md](./DEVELOPMENT.md).
