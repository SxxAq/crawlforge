from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extract_links(base_url: str, html: str) -> list[str]:
    """
    Extract all links from the HTML content.

    Args:
        base_url (str): The base URL for resolving relative links.
        html (str): The HTML content.

    Returns:
        list[str]: A list of extracted links.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if not href or href.startswith("#"):
            continue
        full_url = urljoin(base_url, href)
        links.append(full_url)
    return links


def extract_title(html: str) -> str | None:
    """
    Extract the title from the HTML content.

    Args:
        html (str): The HTML content.

    Returns:
        str|None: The extracted title or None if not found.
    """
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    return title_tag.string if title_tag else None
