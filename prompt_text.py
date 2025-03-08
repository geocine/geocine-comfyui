class PromptText:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True})
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("prompt", )
    FUNCTION = "get_value"
    CATEGORY = "utils"

    def get_value(self, prompt):
        if not prompt:
            return (None, )
        return (prompt, )