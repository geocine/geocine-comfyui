import torch

class ImageSelector:
    CATEGORY = "geocine"
    @classmethod    
    def INPUT_TYPES(s):
        return { "required":  { "images": ("IMAGE",), } }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "choose_image"

    def choose_image(self, images):
        brightness = list(torch.mean(image.flatten()).item() for image in images)
        brightest = brightness.index(max(brightness))
        result = images[brightest].unsqueeze(0)
        return (result,)

