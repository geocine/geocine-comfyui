from .image_selector_node import ImageSelector
from .image_scale_node import ImageScaleNode
from .seed_to_noise import SeedToNoiseNode
from .lora_name_list import LoraNameList
from .show_text_node import ShowTextNode
from .prompt_text import PromptText
from .text_replace import TextReplace
from .openai_compatible_llm import OpenAICompatibleLLM, PreviewText

WEB_DIRECTORY = "js"

NODE_CLASS_MAPPINGS = {
    "Image Selector" : ImageSelector,
    "Image Scale" : ImageScaleNode,
    "Seed to Noise" : SeedToNoiseNode,
    "LoRA Name List" : LoraNameList,
    "ShowTextNode": ShowTextNode,  # Add this line
    "Prompt Text": PromptText,
    "Text Replace": TextReplace,
    "OpenAICompatibleLLM": OpenAICompatibleLLM,
    "PreviewText": PreviewText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShowTextNode": "Show Text",
    "OpenAICompatibleLLM": "OpenAI Compatible LLM",
    "PreviewText": "Preview Text",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
