import torch

class ImageScaleNode:
    CATEGORY = "geocine > scale"
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 32, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 32, "max": 8192}),
            }
        }
    
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT", "INT")
    RETURN_NAMES = ("latent_width", "latent_height", "upscale_by", "tile_width", "tile_height")
    FUNCTION = "scale_image"

    def image_fit(original_width, original_height):
        if original_width / original_height > 1:
            scaling_factor = 512 / original_width
        else:
            scaling_factor = 512 / original_height
        
        new_width = int(original_width * scaling_factor)
        new_height = int(original_height * scaling_factor)

        return new_width, new_height
    
    def scale_image(self, width, height):
        tile_padding = 32
        latent_width, latent_height = ImageScaleNode.image_fit(width, height)
        
        upscale_by = max(width / latent_width, height / latent_height)
        
        tile_width = int(upscale_by * width / 2 + tile_padding)
        tile_height = int(upscale_by * height / 2 + tile_padding)

        print(f"latent_width: {latent_width}, latent_height: {latent_height}, upscale_by: {upscale_by}, tile_width: {tile_width}, tile_height: {tile_height}")
        
        return (latent_width, latent_height, upscale_by, tile_width, tile_height)
