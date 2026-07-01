from .nodes.image.selector import ImageSelector
from .nodes.image.scale import ImageScaleNode
from .nodes.conditioning.turbo_seed_variance import TurboSeedVariance
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
    "TurboSeedVariance": TurboSeedVariance,
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
    "TurboSeedVariance": "Turbo Seed Variance",
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
