from crawlforge.queue.redis_queue import push_url
from crawlforge.utils.url_utils import is_valid_url

url = input("Enter URL: ").strip()
if is_valid_url(url):
    push_url(url)
    print("Queued:", url)
else:
    print("Invalid URL")
