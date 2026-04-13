import json
import os

from crawlforge.ml.vector_store import VectorStore


def build_index(file_path: str = "data/embedded_data.jsonl") -> VectorStore:
    """Build a vector store index from crawled data.

    Args:
        file_path: Path to the JSONL file containing crawled data.

    Returns:
        VectorStore: An indexed vector store with embeddings.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If a line in the file is invalid JSON.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    store = VectorStore()
    records_added = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(
                    f"Invalid JSON on line {line_num}: {str(e)}", line, e.pos
                )

            # Check for required fields
            if "embedding" not in record:
                continue
            if not all(key in record for key in ["url", "title", "content"]):
                continue

            embedding = record.get("embedding")
            if embedding:
                metadata = {
                    "url": record["url"],
                    "title": record["title"],
                    "content": record["content"][:200],  # Store a snippet for reference
                }
                store.add(embedding, metadata)
                records_added += 1

    print(f"Indexed {records_added} records from {file_path}")
    return store
