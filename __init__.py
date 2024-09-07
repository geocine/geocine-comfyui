from .image_selector_node import ImageSelector
from .image_scale_node import ImageScaleNode
from .seed_to_noise import SeedToNoiseNode

NODE_CLASS_MAPPINGS = {
    "Image Selector" : ImageSelector,
    "Image Scale" : ImageScaleNode,
    "Seed to Noise" : SeedToNoiseNode,
}

__all__ = ['NODE_CLASS_MAPPINGS']