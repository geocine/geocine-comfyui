class PreviewText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "format_json": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "preview"
    CATEGORY = "geocine/preview"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def preview(self, text, format_json=False):
        if isinstance(text, (list, tuple)):
            preview_text = "\n\n".join(str(item) for item in text)
        else:
            preview_text = str(text or "")

        return {"ui": {"text": (preview_text,)}, "result": (preview_text,)}
