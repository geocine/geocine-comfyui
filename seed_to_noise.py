from comfy_extras.nodes_custom_sampler import Noise_RandomNoise

class SeedToNoiseNode:
    CATEGORY = "geocine"
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": True}),
            }
        }
    
    RETURN_TYPES = ("NOISE",)
    FUNCTION = "generate_noise"

    def generate_noise(self, seed):
        
        noise = Noise_RandomNoise(seed)
        
        return (noise,)
