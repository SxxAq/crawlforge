import redis

REDIS_QUEUE_KEY = "crawlforge_queue"

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
