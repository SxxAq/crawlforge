import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.data = []

    def add(self, embedding, metadata):
        vector = np.array([embedding]).astype("float32")
        self.index.add(vector)
        self.data.append(metadata)

    def search(self, query_embedding, top_k=5):
        vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(vector, top_k)

        result = []
        for idx in indices[0]:
            if idx < len(self.data):
                result.append(self.data[idx])
        return result
