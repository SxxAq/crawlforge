"""Embedding worker that processes crawled content and generates embeddings."""

import asyncio
from typing import Optional

from crawlforge.ml.embedding_model import EmbeddingModel
from crawlforge.queue.redis_queue import pop_content
from crawlforge.storage.jsonl_writer import JSONLWriter


async def embedding_worker(name: str, stop_event: asyncio.Event) -> None:
    """Process content from Redis queue and generate embeddings.
    
    Args:
        name: Worker identifier for logging.
        stop_event: Event signal to stop the worker.
    """
    print(f"[{name}] Embedding worker started")
    model = EmbeddingModel()
    writer = JSONLWriter("crawled_data.jsonl")

    while not stop_event.is_set():
        record = pop_content()
        if not record:
            await asyncio.sleep(1)
            continue

        url = record.get("url")
        title = record.get("title")
        content = record.get("content")

        if not content:
            continue

        try:
            print(f"[{name}] Processing: {url}")
            
            # Embed content combined with title for better context
            content_to_embed = f"{title} {content[:500]}" if title else content[:500]
            embedding = model.embed(content_to_embed)

            # Create record with all fields including embedding
            embedding_record = {
                "url": url,
                "title": title,
                "content": content,  # Keep full content
                "embedding": embedding,  # Already a list from EmbeddingModel
            }
            await writer.write(embedding_record)
            print(f"[{name}] Embedding saved for: {url}")
            
        except Exception as e:
            print(f"[{name}] Error processing record: {e}")
            continue


async def run_embedding_worker(workers: int = 2, max_duration: int = 300) -> None:
    """Run embedding workers for the specified duration.
    
    Args:
        workers: Number of embedding workers to run.
        max_duration: Maximum runtime in seconds.
    """
    print(f"Starting {workers} embedding workers...")
    stop_event = asyncio.Event()
    
    async def stop_after_duration():
        await asyncio.sleep(max_duration)
        stop_event.set()
    
    tasks = []
    tasks.append(asyncio.create_task(stop_after_duration()))
    
    for i in range(workers):
        task = asyncio.create_task(
            embedding_worker(f"Embedding-Worker-{i+1}", stop_event)
        )
        tasks.append(task)
    
    await asyncio.gather(*tasks, return_exceptions=True)
    print("Embedding workers stopped")


if __name__ == "__main__":
    asyncio.run(run_embedding_worker(workers=2, max_duration=300))
