import aiohttp


async def fetch(session: aiohttp.ClientSession, url: str) -> str | None:
    """
    Fetch the content of a URL ASynchronously.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The content of the URL.
    """
    try:
        headers = {
            "User-Agent": "CrawlForge/1.0 (+https://github.com/SxxAq/crawlforge)"
        }
        async with session.get(
            url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            if response.status != 200:
                print(f"Failed to fetch {url}: HTTP {response.status}")
                return ""

            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")

    return ""
