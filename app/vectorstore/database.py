import json, faiss, numpy as np
from app.services.embedding_service import EmbeddingService
from app.utils.logger import logger

class VectorStoreManager:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.index = None
        self.metadata_store = {}

    def initialize_store(self, json_path: str):
        with open(json_path, 'r') as f: documents = json.load(f)
        chunks = [{"text": doc["content"], "title": doc["title"]} for doc in documents]
        
        # Generates a 3072-dimension matrix automatically
        embeddings_matrix = np.array([self.embedder.generate_embedding(c["text"]) for c in chunks]).astype('float32')
        
        # FAISS builds dynamically based on the matrix shape (embeddings_matrix.shape[1] will be 3072)
        self.index = faiss.IndexFlatIP(embeddings_matrix.shape[1])
        self.index.add(embeddings_matrix)
        
        for idx, chunk in enumerate(chunks): self.metadata_store[idx] = chunk

    # CHANGED: Default threshold lowered to 0.35 to match 3072-dimension scaling
    def search_similarity(self, query: str, top_k: int = 3, threshold: float = 0.0) -> list[dict]:
        if self.index is None: return []
        query_vector = np.array([self.embedder.generate_embedding(query)]).astype('float32')
        scores, indices = self.index.search(query_vector, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and float(score) >= threshold:
                chunk_data = self.metadata_store[idx].copy()
                results.append(chunk_data)
        return results

vector_db = VectorStoreManager()