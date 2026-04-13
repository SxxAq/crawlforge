# CrawlForge Demo — Complete Flow

A working demo of a **distributed web crawler + ML search system** with Redis queue, semantic embeddings, and FastAPI.

---

## Prerequisites

- Docker & Docker Compose installed

---

## Step 1: Start the System

```bash
docker compose up
```

This spins up:
- **Redis** (URL queue & visited set)
- **Crawler** (async workers fetching pages)
- **Embedder** (generates semantic embeddings)
- **API** (FastAPI search engine)

Wait for all services to be healthy (~10-15 seconds). You'll see logs like:
```
crawlforge-redis      | * Ready to accept connections
crawlforge-crawler    | Starting crawler workers...
crawlforge-embedder   | Embedding worker started
crawlforge-api        | Application startup complete
```

---

## Step 2: Seed a URL to Crawl

In a **new terminal**, queue a URL:

```bash
curl -X POST http://localhost:8000/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Machine_learning"}'
```

**Expected response:**
```json
{
  "message": "Queued",
  "url": "https://en.wikipedia.org/wiki/Machine_learning",
  "queue_position": 1
}
```

The crawler will:
1. Fetch the page
2. Extract links and content
3. Store raw data in `crawled_data.jsonl`
4. Push to content queue

---

## Step 3: Watch the Crawler Work

Check the **crawler logs** in the docker-compose terminal—you'll see:

```
[Worker-1] Crawling: https://en.wikipedia.org/wiki/Machine_learning
[Worker-1] Title: Machine learning - Wikipedia
[Worker-1] Content length: 12445 characters
[Worker-1] Data written for: https://en.wikipedia.org/wiki/Machine_learning
```

It extracts links and queues them for discovery (respecting crawl delays).

---

## Step 4: Wait for Embeddings

The **embedding worker** processes crawled content asynchronously:

```
[Embedding-Worker-1] Processing: https://en.wikipedia.org/wiki/Machine_learning
[Embedding-Worker-1] Embedding saved for: https://en.wikipedia.org/wiki/Machine_learning
```

This:
- Reads from Redis content queue
- Generates 384-dim embeddings via sentence-transformers
- Saves to `embedded_data.jsonl`

**⏱️ Wait 30-60 seconds** for embeddings to be written, then the API loads them.

---

## Step 5: Reload the Vector Index

Once embeddings are ready, rebuild the search index:

```bash
curl -X POST http://localhost:8000/reload
```

**Expected response:**
```json
{
  "message": "Reloaded"
}
```

This loads `embedded_data.jsonl` into FAISS for semantic search.

---

## Step 6: Run a Semantic Search

Query for conceptually related content:

```bash
curl "http://localhost:8000/search?query=algorithms+and+data+science"
```

**Expected response:**
```json
{
  "results": [
    {
      "url": "https://en.wikipedia.org/wiki/Machine_learning",
      "title": "Machine learning - Wikipedia",
      "content_snippet": "Machine learning is a subset of artificial intelligence..."
    }
  ],
  "count": 1
}
```

Try other queries:
```bash
curl "http://localhost:8000/search?query=neural+networks"
curl "http://localhost:8000/search?query=statistical+models"
```

---

## Architecture in Action

```
┌─────────────┐
│  Your curl  │
└──────┬──────┘
       │ POST /crawl
       ↓
┌──────────────────┐
│   FastAPI (8000) │
└────────┬─────────┘
         │
         ↓
    ┌────────┐
    │  Redis │
    └────┬───┘
         │
    ┌────┴──────────┐
    ↓               ↓
 Crawler        Content Queue
    │               │
    ├→ fetch        │
    ├→ parse        │
    └→ push links   │
                    ↓
              Embedder
                 │
          ├→ embed text
          └→ save vectors
                 │
                 ↓
          embedded_data.jsonl
                 │
                 ↓
          FAISS Vector Index
                 │
         (loaded on /reload)
                 │
                 ↓
            /search endpoint
```

---

## What This Demonstrates

✅ **Distributed Systems** — Redis queue, async workers, inter-service communication  
✅ **Concurrency** — Multiple crawler workers + embedding workers running in parallel  
✅ **ML Pipeline** — Sentence-transformers embeddings → FAISS vector search  
✅ **API Design** — Clean REST endpoints with proper error handling  
✅ **DevOps** — Docker containerization, service orchestration  
✅ **Data Flow** — HTML → parsing → embeddings → search  

---

## Cleanup

```bash
# Stop all services
docker compose down

# Remove containers and data
docker compose down -v
```

---

## Troubleshooting

**API returns "index not ready yet"**
- Embeddings take time. Wait 30-60 seconds and run `/reload` again.

**curl: (7) Failed to connect**
- Docker services still starting. Wait 15 seconds and retry.

**No search results**
- Only 1 page crawled. Queue more URLs or restart `docker compose` and seed multiple sites.

---