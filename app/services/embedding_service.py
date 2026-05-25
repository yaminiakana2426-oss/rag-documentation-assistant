import os
from google import genai

class EmbeddingService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def generate_embedding(self, text: str) -> list[float]:
        # gemini-embedding-001 is the active stable model on v1beta
        response = self.client.models.embed_content(model="gemini-embedding-001", contents=text)
        return response.embeddings[0].values