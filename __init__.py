from .image_selector_node import ImageSelector
from .image_scale_node import ImageScaleNode
from .seed_to_noise import SeedToNoiseNode
from .lora_name_list import LoraNameList
from .lora_loader_node import LoraLoaderStack
from .show_text_node import ShowTextNode
from .prompt_text import PromptText
from .text_replace import TextReplace
from .openai_compatible_llm import OpenAICompatibleLLM, PreviewText

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "ImageSelector": ImageSelector,
    "ImageScale": ImageScaleNode,
    "SeedToNoise": SeedToNoiseNode,
    "LoraNameList": LoraNameList,
    "LoraLoaderStack": LoraLoaderStack,
    "ShowTextNode": ShowTextNode,
    "PromptText": PromptText,
    "TextReplace": TextReplace,
    "OpenAICompatibleLLM": OpenAICompatibleLLM,
    "PreviewText": PreviewText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageSelector": "Image Selector",
    "ImageScale": "Image Scale",
    "SeedToNoise": "Seed to Noise",
    "LoraNameList": "LoRA Name List",
    "LoraLoaderStack": "LoRA Loader Stack",
    "ShowTextNode": "Show Text",
    "PromptText": "Prompt Text",
    "TextReplace": "Text Replace",
    "OpenAICompatibleLLM": "OpenAI Compatible LLM",
    "PreviewText": "Preview Text",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
