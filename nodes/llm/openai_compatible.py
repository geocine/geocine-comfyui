class OpenAICompatibleLLM:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "system_prompt": ("STRING", {"multiline": True, "default": ""}),
                "api_key": ("STRING", {"default": ""}),
                "base_url": ("STRING", {"default": "http://localhost:1234/v1"}),
                "model": ("STRING", {"default": "gpt-4.1-mini"}),
                "temperature": (
                    "FLOAT",
                    {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1},
                ),
                "max_tokens": ("INT", {"default": 512, "min": 1, "max": 32768}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "generate"
    CATEGORY = "geocine/llm"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def generate(
        self,
        prompt,
        system_prompt,
        api_key,
        base_url,
        model,
        temperature,
        max_tokens,
    ):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError(
                "OpenAI Compatible LLM requires the 'openai' package. "
                "Install it with: python -m pip install openai"
            ) from exc

        client = OpenAI(
            base_url=base_url.strip(),
            api_key=(api_key or "").strip() or "not-needed",
        )

        messages = []
        if system_prompt and system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt or ""})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return (response.choices[0].message.content or "",)
