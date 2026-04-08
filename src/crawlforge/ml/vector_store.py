from typing import Any, List, Optional

import faiss
import numpy as np


class VectorStore:
    """Vector store using FAISS for semantic search."""

    def __init__(self, dim: int = 384) -> None:
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.data: List[dict] = []

    def add(self, embedding: List[float], metadata: dict) -> None:
        """Add an embedding and its metadata to the store.

        Args:
            embedding: List of float values representing the vector.
            metadata: Dictionary containing associated data (url, title, content, etc).
        """
        vector = np.array([embedding]).astype("float32")
        self.index.add(vector)
        self.data.append(metadata)

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[dict]:
        """Search for the most similar embeddings.

        Args:
            query_embedding: Query vector as a list of floats.
            top_k: Number of top results to return.

        Returns:
            List of metadata dictionaries for the top_k matches.
        """
        if not self.data:
            return []
        top_k = min(top_k, len(self.data))

        vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(vector, top_k)

        result = []
        for idx in indices[0]:
            if 0 <= idx < len(self.data):
                result.append(self.data[idx])
        return result
