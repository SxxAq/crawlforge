import asyncio
import time


class DomainScheduler:
    def __init__(self, crawl_delay: float = 1.0):
        self.crawl_delay = crawl_delay
        self.domain_last_access = {}
        self.lock = asyncio.Lock()

    async def wait_for_domain(self, domain: str):
        async with self.lock:
            now = time.time()
            last_access = self.domain_last_access.get(domain, 0)
            elapsed = now - last_access
            if elapsed < self.crawl_delay:
                wait_time = self.crawl_delay - elapsed
                await asyncio.sleep(wait_time)
            self.domain_last_access[domain] = time.time()
