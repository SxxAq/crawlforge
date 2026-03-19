from typing import List

from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()
