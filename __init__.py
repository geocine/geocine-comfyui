from .nodes.image.selector import ImageSelector
from .nodes.image.scale import ImageScaleNode
from .nodes.conditioning.seed_variance_enhancer import SeedVarianceEnhancer
from .nodes.sampling.seed_to_noise import SeedToNoiseNode
from .nodes.lora.name_list import LoraNameList
from .nodes.lora.loader_stack import LoraLoaderStack
from .nodes.text.show import ShowTextNode
from .nodes.text.prompt import PromptText
from .nodes.text.replace import TextReplace
from .nodes.text.preview import PreviewText
from .nodes.llm.openai_compatible import OpenAICompatibleLLM

WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "ImageSelector": ImageSelector,
    "ImageScale": ImageScaleNode,
    "SeedVarianceEnhancer": SeedVarianceEnhancer,
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
    "SeedVarianceEnhancer": "Seed Variance Enhancer",
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
