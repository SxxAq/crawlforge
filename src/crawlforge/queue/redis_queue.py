import redis

REDIS_QUEUE_KEY = "crawlforge_queue"
VISITED_SET_KEY = "visited_urls"
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def push_url(url: str):
    """Push a URL to the Redis queue."""
    r.lpush(REDIS_QUEUE_KEY, url)


def pop_url():
    """Pop a URL from the Redis queue."""
    return r.rpop(REDIS_QUEUE_KEY)


def queue_size():
    """Get the current size of the Redis queue."""
    return r.llen(REDIS_QUEUE_KEY)


def mark_visited(url: str):
    """Mark a URL as Visited."""
    r.sadd(VISITED_SET_KEY, url)


def is_visited(url: str):
    """Check if a URL has been visited."""
    return r.sismember(VISITED_SET_KEY, url)
