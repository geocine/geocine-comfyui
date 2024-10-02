from .image_selector_node import ImageSelector
from .image_scale_node import ImageScaleNode
from .seed_to_noise import SeedToNoiseNode
from .lora_name_list import LoraNameList

WEB_DIRECTORY = "js"

NODE_CLASS_MAPPINGS = {
    "Image Selector" : ImageSelector,
    "Image Scale" : ImageScaleNode,
    "Seed to Noise" : SeedToNoiseNode,
    "LoRA Name List" : LoraNameList,
}

__all__ = ['NODE_CLASS_MAPPINGS']