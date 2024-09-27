import folder_paths
from nodes import LoraLoader

MAX_LORAS = 20

class LoraCycler(LoraLoader):

    @classmethod
    def INPUT_TYPES(cls):
        loras = ["None"] + folder_paths.get_filename_list("loras")
        inputs = {
            "required": {
                "model": ("MODEL",),
                "lora_count": ("INT", {"default": 3, "min": 1, "max": 20, "step": 1}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01})
            }
        }
        
        # Add 20 LoRA inputs
        for i in range(1, MAX_LORAS+1):
            inputs["required"][f"lora_name_{i}"] = (loras,)
    
        return inputs

    RETURN_TYPES = ("MODEL", "STRING", "INT")
    RETURN_NAMES = ("Model", "Lora Name", "Split Size")
    OUTPUT_IS_LIST = (False, True, True)
    FUNCTION = "cycle_loras"

    CATEGORY = "LoRA"

    def cycle_loras(self, model, lora_count, strength_model, **kwargs):
        lora_list = []
        for i in range(1, lora_count + 1):
            lora_name = kwargs.get(f"lora_name_{i}")
            if lora_name and lora_name != "None":
                lora_list.append(lora_name)
        
        for lora_name in lora_list:
            model = self.load_lora(model, None, lora_name, strength_model, 0)[0]
        
        return (model, lora_list, [1] * lora_count)
