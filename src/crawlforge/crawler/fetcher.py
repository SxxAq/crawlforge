import httpx

def fetch(url: str) -> str:
    """
    Fetch the content of a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The content of the URL.
    """
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.text
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
    return ""