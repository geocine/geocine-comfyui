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
    "GeocineImageSelector": ImageSelector,
    "GeocineImageScale": ImageScaleNode,
    "GeocineTurboSeedVariance": TurboSeedVariance,
    "GeocineSeedToNoise": SeedToNoiseNode,
    "GeocineLoraNameList": LoraNameList,
    "GeocineLoraLoaderStack": LoraLoaderStack,
    "GeocineShowTextNode": ShowTextNode,
    "GeocinePromptText": PromptText,
    "GeocineTextReplace": TextReplace,
    "GeocineOpenAICompatibleLLM": OpenAICompatibleLLM,
    "GeocinePreviewText": PreviewText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeocineImageSelector": "Image Selector",
    "GeocineImageScale": "Image Scale",
    "GeocineTurboSeedVariance": "Turbo Seed Variance",
    "GeocineSeedToNoise": "Seed to Noise",
    "GeocineLoraNameList": "LoRA Name List",
    "GeocineLoraLoaderStack": "LoRA Loader Stack",
    "GeocineShowTextNode": "Show Text",
    "GeocinePromptText": "Prompt Text",
    "GeocineTextReplace": "Text Replace",
    "GeocineOpenAICompatibleLLM": "OpenAI Compatible LLM",
    "GeocinePreviewText": "Preview Text",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
