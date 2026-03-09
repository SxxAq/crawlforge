import asyncio
import aiohttp

from crawlforge.crawler.fetcher import fetch
from crawlforge.parser.html_parser import extract_links, extract_title
from crawlforge.utils.url_utils import normalize_url, get_domain


async def worker(
    name, session, queue, visited, visited_lock, allowed_domain, max_pages, stop_event
):
    while not stop_event.is_set():
        try:
            url = await asyncio.wait_for(queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            continue

        try:
            url = normalize_url(url)

            # Thread-safe check and add to visited
            async with visited_lock:
                if url in visited or len(visited) >= max_pages:
                    queue.task_done()
                    continue
                visited.add(url)

            if get_domain(url) != allowed_domain:
                queue.task_done()
                continue

            print(f"[{name}] Crawling: {url}")
            html = await fetch(session, url)
            if not html:
                queue.task_done()
                continue

            title = extract_title(html)
            print(f"\n[{name}] Title: {title}")

            async with visited_lock:
                print(f"\n[{name}] Visited: {len(visited)} pages")

            links = extract_links(url, html)
            for link in links:
                normalized = normalize_url(link)
                async with visited_lock:
                    if normalized not in visited and len(visited) < max_pages:
                        await queue.put(normalized)

            queue.task_done()
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[{name}] Error: {e}")
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
    visited_lock = asyncio.Lock()
    stop_event = asyncio.Event()

    async with aiohttp.ClientSession() as session:

        tasks = []
        for i in range(workers):
            task = asyncio.create_task(
                worker(
                    f"Worker-{i+1}",
                    session,
                    queue,
                    visited,
                    visited_lock,
                    allowed_domain,
                    max_pages,
                    stop_event,
                )
            )
            tasks.append(task)

        await queue.join()

        # Signal workers to stop gracefully
        stop_event.set()

        # Wait for all workers to finish
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(crawl("https://github.com/SxxAq", max_pages=10))
