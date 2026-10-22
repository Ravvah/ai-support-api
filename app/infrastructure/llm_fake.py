class FakeLLM:
    def generate(self, prompt: str) -> str:
        return f"FAKE : {prompt}"
