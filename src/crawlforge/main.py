from crawlforge.crawler.fetcher import fetch
from crawlforge.parser.html_parser import extract_links, extract_title
from crawlforge.utils.url_utils import normalize_url, get_domain, is_same_domain


def crawl(seed_url: str, max_pages: int = 20):
    """Basic BFS web crawler.
    Args:
        seed_url (str): The starting URL for crawling.
        max_pages (int): The maximum number of pages to crawl.

    Returns:
        None
    """

    seed_url = normalize_url(seed_url)
    allowed_domain = get_domain(seed_url)

    queue = [seed_url]
    visited = set()

    while queue and len(visited) < max_pages:
        url = normalize_url(queue.pop(0))
        print("Queue size:", len(queue))
        if url in visited:
            continue

        if get_domain(url) != allowed_domain:
            continue

        print(f"\nCrawling: {url}")
        html = fetch(url)

        if not html:
            continue

        visited.add(url)
        title = extract_title(html)

        print(f"\nTitle: {title}")

        links = extract_links(url, html)
        for link in links:
            normalized = normalize_url(link)
            if normalized not in visited:
                queue.append(normalized)

        print(f"\nVisited: {len(visited)} pages")


if __name__ == "__main__":
    crawl("https://github.com/SxxAq", max_pages=10)
