from .image_selector_node import ImageSelector
from .image_scale_node import ImageScaleNode

NODE_CLASS_MAPPINGS = {
    "Image Selector (geocine)" : ImageSelector,
    "Image Scale (geocine)" : ImageScaleNode,
}

__all__ = ['NODE_CLASS_MAPPINGS']