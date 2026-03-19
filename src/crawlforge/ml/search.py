from crawlforge.ml.build_index import build_index
from crawlforge.ml.embedding_model import EmbeddingModel


def search(query: str, file_path: str = "crawled_data.jsonl") -> None:
    """Search for similar documents using semantic embeddings.

    Args:
        query: The search query string.
        file_path: Path to the JSONL file containing crawled data.
    """
    try:
        model = EmbeddingModel()
        store = build_index(file_path)

        if not store.data:
            print("Error: No data indexed. Please check your data file.")
            return

        query_embedding = model.embed(query)
        results = store.search(query_embedding, top_k=5)

        if not results:
            print("No results found for your query.")
            return

        print(f"\nFound {len(results)} results for '{query}':")
        for i, res in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"URL: {res['url']}")
            print(f"Title: {res['title']}")
            print(f"Content Snippet: {res['content']}...\n")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error during search: {e}")


if __name__ == "__main__":
    query = input("Enter your search query: ")
    search(query)
