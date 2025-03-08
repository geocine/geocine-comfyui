from .image_selector_node import ImageSelector
from .image_scale_node import ImageScaleNode
from .seed_to_noise import SeedToNoiseNode
from .lora_name_list import LoraNameList
from .show_text_node import ShowTextNode
from .prompt_text import PromptText
from .text_replace import TextReplace

WEB_DIRECTORY = "js"

NODE_CLASS_MAPPINGS = {
    "Image Selector" : ImageSelector,
    "Image Scale" : ImageScaleNode,
    "Seed to Noise" : SeedToNoiseNode,
    "LoRA Name List" : LoraNameList,
    "ShowTextNode": ShowTextNode,  # Add this line
    "Prompt Text": PromptText,
    "Text Replace": TextReplace,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShowTextNode": "Show Text",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']