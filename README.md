# CrawlForge

**CrawlForge** is a distributed web crawling system designed to efficiently collect and process web data at scale.

It leverages asynchronous workers, a Redis-based URL frontier, and a decoupled pipeline for crawling, content extraction, and embedding generation. This architecture enables scalable processing across multiple processes or machines while maintaining clear separation between I/O-bound and compute-bound tasks.

The project demonstrates core backend and data engineering concepts such as **distributed systems, asynchronous networking, queue-based task distribution, and data pipelines**. It is designed to be extensible for applications like **dataset generation, search indexing, and semantic retrieval systems**.

---

## Architecture

CrawlForge uses a **three-stage distributed pipeline** with Redis as the central broker and FAISS for semantic search:

```
┌──────────────────────────────────────────────────────────────┐
│                     Redis                                    │
│  (URL Queue + Content Queue + Visited Set)                  │
└──────────────┬─────────────────────────┬────────────────────┘
               │                         │
        ┌──────▼─────────┐    ┌─────────▼──────────┐
        │  Crawler Svc   │    │  Embedder Svc      │
        │                │    │                    │
        │ - Pop URL      │    │ - Pop content      │
        │ - Fetch page   │    │ - Generate embed   │
        │ - Extract text │    │ - Write JSONL      │
        │ - Push content │    │                    │
        └────────────────┘    └─────────┬──────────┘
                                        │
                                ┌───────▼────────┐
                                │  embedded_data │
                                │      .jsonl    │
                                └───────┬────────┘
                                        │
                                ┌───────▼────────┐
        ┌──────────────────────▶│  FAISS Index   │
        │                       └────────────────┘
        │                              │
        └──────────────────────────────┘
       (Index reloaded every 30s)

    ┌──────────────────────┐
    │    API Service       │
    │  (port 8000)         │
    │  - /crawl (POST)     │
    │  - /search (GET)     │
    │  - /reload (POST)    │
    └──────────────────────┘
           │
        Client
```

### Workflow

1. **Crawl Phase**: Seed URLs → URL queue → Crawler service fetches pages concurrently
2. **Parse Phase**: HTML parsed → main text extracted → pushed to content queue
3. **Embed Phase**: Embedder service reads content queue → generates 384-dim vectors → writes to `data/embedded_data.jsonl`
4. **Index Phase**: Every 30s, API reloads FAISS index from embedded_data.jsonl
5. **Search Phase**: User queries API → semantic search via FAISS → ranked results returned

### Data Flow

- **URL Queue** (Redis): Stores frontier URLs to crawl
- **Content Queue** (Redis): Stores extracted text from pages
- **crawled_data.jsonl**: Raw HTML + metadata from crawler (optional storage)
- **embedded_data.jsonl**: Embeddings + metadata for semantic search
- **FAISS Index**: In-memory vector index for fast similarity search

---

## Project Structure

```
crawlforge/
│
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── DEMO.md
├── README.md
│
├── data/                    # Persistent volume (synced from containers)
│   ├── crawled_data.jsonl
│   └── embedded_data.jsonl
│
└── src/crawlforge/
    ├── main.py              # Crawler entry point
    ├── seed_url.py          # Interactive URL seeding
    │
    ├── api/
    │   └── search_api.py    # FastAPI server (/crawl, /search, /reload)
    │
    ├── crawler/
    │   └── fetcher.py       # Async HTTP fetch with User-Agent
    │
    ├── parser/
    │   ├── html_parser.py   # Extract links, title
    │   └── content_extractor.py  # Extract main content
    │
    ├── queue/
    │   └── redis_queue.py   # Redis URL queue operations
    │
    ├── scheduler/
    │   └── domain_scheduler.py  # Rate limiting per domain
    │
    ├── storage/
    │   └── jsonl_writer.py  # Async JSONL file writing
    │
    ├── ml/
    │   ├── embedding_model.py   # sentence-transformers wrapper
    │   ├── embedding_worker.py  # Async embedding processing
    │   ├── build_index.py       # Load embeddings → FAISS
    │   ├── vector_store.py      # FAISS wrapper
    │   └── search.py            # CLI semantic search
    │
    └── utils/
        └── url_utils.py     # URL normalization, validation
```

---

## Tech Stack

**Language & Async**
- Python 3.12
- asyncio, aiohttp

**Web Parsing**
- BeautifulSoup
- readability-lxml

**Infrastructure**
- Redis (URL frontier & queue)
- FastAPI (search API)
- Docker & Docker Compose

**ML/Search**
- sentence-transformers (embeddings)
- FAISS (vector indexing)

---

## Getting Started

### Docker (Recommended)

Clone the repository:

```bash
git clone https://github.com/SxxAq/crawlforge.git
cd crawlforge
```

Start all services:

```bash
mkdir -p data
docker compose up
```

In another terminal, queue a URL:

```bash
curl -X POST http://localhost:8000/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Machine_learning"}'
```

Wait 30-60 seconds for embeddings, then search:

```bash
curl "http://localhost:8000/search?query=machine+learning"
```

See [DEMO.md](./DEMO.md) for step-by-step walkthrough.

### Local Development (requires Redis)

Install dependencies:

```bash
uv sync
```

Start Redis (separate terminal):

```bash
redis-server
```

Run crawler:

```bash
python -m crawlforge.main
```

Run embedder (separate terminal):

```bash
python -m crawlforge.ml.embedding_worker
```

Run API (separate terminal):

```bash
uvicorn crawlforge.api.search_api:app --reload
```
