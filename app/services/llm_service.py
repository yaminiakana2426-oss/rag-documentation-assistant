import os
from google import genai
from google.genai import types
from app.prompts.rag_templates import SYSTEM_INSTRUCTION
class LLMService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    def generate_response(self, prompt: str) -> tuple[str, int]:
        config = types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION, temperature=0.1)
        response = self.client.models.generate_content(model="gemini-2.5-flash", contents=prompt, config=config)
        tokens = response.usage_metadata.total_token_count if response.usage_metadata else 0
        return response.text, tokens