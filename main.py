import asyncio

from src.crawlforge.main import crawl
from src.crawlforge.queue.redis_queue import push_url


def main():
    # Seed a URL into the crawler queue
    push_url("https://example.com")
    # Start the crawler (runs for 300 seconds by default with 5 workers)
    asyncio.run(crawl())


if __name__ == "__main__":
    main()
