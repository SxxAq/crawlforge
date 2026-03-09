import asyncio
import aiohttp

from crawlforge.crawler.fetcher import fetch
from crawlforge.parser.html_parser import extract_links, extract_title
from crawlforge.utils.url_utils import normalize_url, get_domain


async def worker(name, session, queue, visited, allowed_domain, max_pages):
    while True:
        if len(visited) >= max_pages:
            return
        url = await queue.get()
        url = normalize_url(url)
        if url in visited:
            queue.task_done()
            continue
        if get_domain(url) != allowed_domain:
            queue.task_done()
            continue
        print(f"[{name}] Crawling: {url}")
        html = await fetch(session, url)
        if not html:
            queue.task_done()
            continue
        visited.add(url)
        title = extract_title(html)
        print(f"\n[{name}] Title: {title}")
        print(f"\n[{name}] Visited: {len(visited)} pages")
        links = extract_links(url, html)
        for link in links:
            normalized = normalize_url(link)
            if normalized not in visited:
                await queue.put(normalized)
        queue.task_done()


async def crawl(seed_url: str, max_pages: int = 20, workers: int = 5):
    """Basic BFS web crawler.
    Args:
        seed_url (str): The starting URL for crawling.
        max_pages (int): The maximum number of pages to crawl.
        workers (int): The number of concurrent workers to use.

    Returns:
        None
    """

    seed_url = normalize_url(seed_url)
    allowed_domain = get_domain(seed_url)

    queue = asyncio.Queue()
    await queue.put(seed_url)
    visited = set()
    async with aiohttp.ClientSession() as session:

        tasks = []
        for i in range(workers):
            task = asyncio.create_task(
                worker(
                    f"Worker-{i+1}", session, queue, visited, allowed_domain, max_pages
                )
            )
            tasks.append(task)

        await queue.join()

        for task in tasks:
            task.cancel()


if __name__ == "__main__":
    asyncio.run(crawl("https://github.com/SxxAq", max_pages=10))
