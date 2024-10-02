import folder_paths

MAX_LORAS = 20

class LoraNameList():

    @classmethod
    def INPUT_TYPES(cls):
        loras = ["None"] + folder_paths.get_filename_list("loras")
        inputs = {
            "required": {
                "lora_count": ("INT", {"default": 3, "min": 1, "max": MAX_LORAS, "step": 1}),
            }
        }
        
        # Add 20 LoRA inputs
        for i in range(1, MAX_LORAS+1):
            inputs["required"][f"lora_name_{i}"] = (loras,)
    
        return inputs

    RETURN_TYPES = ("LIST",)
    FUNCTION = "list_loras"
    CATEGORY = "LoRA"

    def list_loras(self, lora_count, **kwargs):
        lora_list = []
        for i in range(1, lora_count + 1):
            lora_name = kwargs.get(f"lora_name_{i}")
            if lora_name and lora_name != "None":
                lora_list.append(lora_name)
        
        return (lora_list,)
