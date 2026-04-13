import asyncio
import aiohttp

from crawlforge.crawler.fetcher import fetch
from crawlforge.parser.html_parser import extract_links, extract_title
from crawlforge.utils.url_utils import normalize_url, get_domain, is_valid_url
from crawlforge.queue.redis_queue import (
    pop_url,
    push_url,
    mark_visited,
    is_visited,
    push_content,
    content_queue_size,
)
from crawlforge.scheduler.domain_scheduler import DomainScheduler
from crawlforge.parser.content_extractor import extract_content
from crawlforge.storage.jsonl_writer import JSONLWriter

MAX_QUEUE_SIZE = 1000
MAX_LINKS_PER_PAGE = 50


async def worker(name, session, scheduler, writer, stop_event):
    print(f"[{name}] Worker started")
    while not stop_event.is_set():
        url = pop_url()
        if not url:
            await asyncio.sleep(1)
            continue

        url = normalize_url(url)
        print(f"[{name}] Popped URL: {url}")

        if not is_valid_url(url):
            continue

        if is_visited(url):
            continue

        print(f"[{name}] Crawling: {url}")

        domain = get_domain(url)
        await scheduler.wait_for_domain(domain)

        html = await fetch(session, url)
        if not html:
            continue

        mark_visited(url)

        title = extract_title(html)
        content = extract_content(html)
        print(f"\n[{name}] Title: {title}")
        print(f"[{name}] Content length: {len(content)} characters\n")

        record = {"url": url, "title": title, "content": content}
        await writer.write(record)
        push_content(record)
        print(f"[{name}] Data written for: {url}")

        links = extract_links(url, html)[:MAX_LINKS_PER_PAGE]
        for link in links:
            normalized = normalize_url(link)
            if not is_valid_url(normalized):
                continue
            if not is_visited(normalized):
                push_url(normalized)


async def crawl(workers: int = 5, max_duration: int = 300):
    """Run crawler workers that consume URLs from Redis."""
    print("Starting crawler workers...")

    scheduler = DomainScheduler(crawl_delay=1.0)
    writer = JSONLWriter("data/crawled_data.jsonl")
    stop_event = asyncio.Event()

    async def stop_after_duration():
        await asyncio.sleep(max_duration)
        stop_event.set()

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(stop_after_duration())]

        for i in range(workers):
            task = asyncio.create_task(
                worker(
                    f"Worker-{i+1}",
                    session,
                    scheduler,
                    writer,
                    stop_event,
                )
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)

    print(f"Crawler stopped. Total records in queue: {content_queue_size()}")


if __name__ == "__main__":
    asyncio.run(crawl())
