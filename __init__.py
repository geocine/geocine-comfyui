from .image_selector_node import ImageSelector
from .image_scale_node import ImageScaleNode
from .seed_to_noise import SeedToNoiseNode
from .lora_cycler import LoraCycler

WEB_DIRECTORY = "js"

NODE_CLASS_MAPPINGS = {
    "Image Selector" : ImageSelector,
    "Image Scale" : ImageScaleNode,
    "Seed to Noise" : SeedToNoiseNode,
    "Lora Cycler" : LoraCycler,
}

__all__ = ['NODE_CLASS_MAPPINGS']