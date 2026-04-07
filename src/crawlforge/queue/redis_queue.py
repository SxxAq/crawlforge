import json
from typing import Optional

import redis

REDIS_QUEUE_KEY = "crawlforge_queue"
CONTENT_QUEUE_KEY = "content_queue"
VISITED_SET_KEY = "visited_urls"
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def push_url(url: str) -> None:
    """Push a URL to the Redis queue."""
    r.lpush(REDIS_QUEUE_KEY, url)


def pop_url() -> Optional[str]:
    """Pop a URL from the Redis queue."""
    return r.rpop(REDIS_QUEUE_KEY)


def queue_size() -> int:
    """Get the current size of the Redis queue."""
    return r.llen(REDIS_QUEUE_KEY)


def mark_visited(url: str) -> None:
    """Mark a URL as Visited."""
    r.sadd(VISITED_SET_KEY, url)


def is_visited(url: str) -> bool:
    """Check if a URL has been visited."""
    return r.sismember(VISITED_SET_KEY, url)


def push_content(record: dict) -> None:
    """Push a content record to the Redis content queue."""
    r.lpush(CONTENT_QUEUE_KEY, json.dumps(record))


def pop_content() -> Optional[dict]:
    """Pop a content record from the Redis content queue."""
    record_json = r.rpop(CONTENT_QUEUE_KEY)
    return json.loads(record_json) if record_json else None


def content_queue_size() -> int:
    """Get the current size of the Redis content queue."""
    return r.llen(CONTENT_QUEUE_KEY)
