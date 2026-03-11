from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    """
    Normalize a URL by removing fragments and query parameters.

    Args:
        url (str): The URL to normalize.

    Returns:
        str: The normalized URL.
    """
    parsed = urlparse(url)
    normalized = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))
    return normalized


def get_domain(url: str) -> str:
    """
    Extract the domain from a URL.

    Args:
        url (str): The URL to extract the domain from.

    Returns:
        str: The extracted domain.
    """
    parsed = urlparse(url)
    return parsed.netloc


def is_same_domain(url1: str, url2: str) -> bool:
    """
    Check if two URLs belong to the same domain.

    Args:
        url1 (str): The first URL.
        url2 (str): The second URL.

    Returns:
        bool: True if both URLs belong to the same domain, False otherwise.
    """
    return get_domain(url1) == get_domain(url2)


def is_valid_url(url: str) -> bool:

    blocked_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".webp",
        ".mp4",
        ".avi",
        ".mov",
        ".wmv",
        ".flv",
        ".mp3",
        ".wav",
        ".pdf",
        ".css",
        ".js",
        ".zip",
        ".ico",
    }
    return not any(url.lower().endswith(ext) for ext in blocked_extensions)
