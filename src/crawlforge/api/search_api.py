import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from crawlforge.ml.embedding_model import EmbeddingModel
from crawlforge.ml.build_index import build_index
from crawlforge.queue.redis_queue import push_url, queue_size
from crawlforge.utils.url_utils import is_valid_url

app = FastAPI()

model = EmbeddingModel()
store = build_index()


class CrawlRequest(BaseModel):
    url: str


async def reload_store():
    while True:
        await asyncio.sleep(30)
        try:
            global store
            store = build_index()
            print("✓ Store reloaded")
        except Exception as e:
            print(f"✗ Reload error: {e}")


@app.on_event("startup")
async def startup():
    asyncio.create_task(reload_store())


@app.post("/crawl")
async def crawl(req: CrawlRequest):
    if not req.url or not is_valid_url(req.url):
        raise HTTPException(400, "Invalid URL")

    try:
        push_url(req.url)
        return {
            "message": "Queued",
            "url": req.url,
            "queue_position": queue_size(),
        }
    except ConnectionError:
        raise HTTPException(503, "Queue unavailable")


@app.get("/search")
async def search(query: str):
    if not query or len(query.strip()) < 2:
        raise HTTPException(400, "Query too short")

    try:
        emb = model.embed(query)
        results = store.search(emb, top_k=5)

        return {
            "results": [
                {
                    "url": r["url"],
                    "title": r["title"],
                    "content_snippet": r["content"][:200],
                }
                for r in results
            ],
            "count": len(results),
        }
    except Exception as e:
        raise HTTPException(500, f"Search error: {e}")


@app.post("/reload")
async def reload_index():
    try:
        global store
        store = build_index()
        return {"message": "Reloaded"}
    except FileNotFoundError:
        raise HTTPException(404, "Data not found")
    except Exception as e:
        raise HTTPException(500, f"Reload error: {e}")
