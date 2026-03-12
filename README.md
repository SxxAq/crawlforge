# CrawlForge

**CrawlForge** is a distributed web crawling system designed to efficiently collect and process web data at scale.
It uses asynchronous workers, a centralized URL frontier, and modular parsing pipelines to enable scalable crawling across multiple processes or machines.

The project demonstrates core backend and data engineering concepts including **distributed systems, asynchronous networking, queue-based task distribution, and data pipelines**. It is designed to be extensible into applications such as **dataset generation, search indexing, and semantic retrieval systems**.

---

## Architecture

The crawler follows a distributed worker architecture where multiple workers fetch and process pages concurrently while sharing a central URL queue.

```
Seed URLs
    |
URL Scheduler
    |
URL Frontier (Queue)
    |
+-----------+-----------+-----------+
| Worker 1  | Worker 2  | Worker 3  |
+-----------+-----------+-----------+
        |
     Parser
        |
   Data Storage
```

## Final Architecture (Complete System)
```
                Seed URLs
                     ↓
               URL Scheduler
                     ↓
                   Redis
            (Distributed Frontier)
                     ↓
      ---------------------------------
      |               |               |
   Worker A        Worker B        Worker C
      |               |               |
     Fetch           Fetch           Fetch
      ↓               ↓               ↓
     Parser          Parser          Parser
      ↓               ↓               ↓
   Clean Text      Clean Text      Clean Text
      ↓               ↓               ↓
   Embeddings       Embeddings       Embeddings
      ↓               ↓               ↓
           Vector Database (Search)
                     ↓
                 FastAPI
                     ↓
                  Clients
```


### Workflow

1. Seed URLs are added to the URL frontier.
2. Workers fetch URLs from the queue.
3. Pages are downloaded asynchronously.
4. HTML content is parsed to extract links and metadata.
5. Newly discovered links are pushed back into the queue.
6. Extracted data is stored for downstream processing.

---

## Project Structure

```
crawlforge/
│
├── pyproject.toml
├── README.md
├── .python-version
│
└── src/
    └── crawlforge/
        ├── main.py
        │
        ├── crawler/
        │   └── fetcher.py
        │
        ├── parser/
        │   └── html_parser.py
        │
        └── utils/
            └── url_utils.py
```

---

## Tech Stack

**Language**

- Python

**Networking**

- httpx

**HTML Parsing**

- BeautifulSoup

**Planned Infrastructure**

- Redis (URL frontier / queue)
- PostgreSQL (content storage)
- FastAPI (search API)
- Docker (containerization)

---

## Getting Started

Clone the repository:

```
git clone https://github.com/<your-username>/crawlforge.git
cd crawlforge
```

Install dependencies using **uv**:

```
uv sync
```

Run the crawler:

```
uv run python src/crawlforge/main.py
```

---

## Roadmap

Planned improvements include:

- asynchronous crawling with `aiohttp`
- Redis-based distributed URL scheduling
- global deduplication system
- domain-aware rate limiting
- content storage in PostgreSQL
- vector embeddings for semantic search
- FastAPI search interface
- Docker-based distributed deployment

---

## License

MIT License
