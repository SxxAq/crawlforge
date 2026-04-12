import json
from typing import Optional, cast
import os
import redis

REDIS_QUEUE_KEY = "crawlforge_queue"
CONTENT_QUEUE_KEY = "content_queue"
VISITED_SET_KEY = "visited_urls"
host = os.getenv("REDIS_HOST", "localhost")
port = int(os.getenv("REDIS_PORT", "6379"))
r = redis.Redis(host=host, port=port, decode_responses=True)


def push_url(url: str) -> None:
    """Push a URL to the Redis queue."""
    r.lpush(REDIS_QUEUE_KEY, url)


def pop_url() -> Optional[str]:
    """Pop a URL from the Redis queue."""
    return cast(Optional[str], r.rpop(REDIS_QUEUE_KEY))


def queue_size() -> int:
    """Get the current size of the Redis queue."""
    return cast(int, r.llen(REDIS_QUEUE_KEY))


def mark_visited(url: str) -> None:
    """Mark a URL as Visited."""
    r.sadd(VISITED_SET_KEY, url)


def is_visited(url: str) -> bool:
    """Check if a URL has been visited."""
    return bool(r.sismember(VISITED_SET_KEY, url))


def push_content(record: dict) -> None:
    """Push a content record to the Redis content queue."""
    r.lpush(CONTENT_QUEUE_KEY, json.dumps(record))


def pop_content() -> Optional[dict]:
    """Pop a content record from the Redis content queue."""
    record_json = cast(Optional[str], r.rpop(CONTENT_QUEUE_KEY))
    if record_json is None:
        return None
    return json.loads(record_json)


def content_queue_size() -> int:
    """Get the current size of the Redis content queue."""
    return cast(int, r.llen(CONTENT_QUEUE_KEY))
