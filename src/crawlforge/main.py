from crawlforge.crawler.fetcher import fetch
from crawlforge.parser.html_parser import extract_links, extract_title

def crawl(seed_url:str,max_pages:int=20):
  """Basic BFS web crawler.
    Args:
        seed_url (str): The starting URL for crawling.
        max_pages (int): The maximum number of pages to crawl.

    Returns:
        None
    """
  queue=[seed_url]
  visited=set()
  
  while queue and len(visited)<max_pages:
    url=queue.pop(0)
    if url in visited:
      continue
    print(f"\nCrawling: {url}")
    html=fetch(url)
    if not html:
      continue
    visited.add(url)
    title=extract_title(html)
    print(f"\nTitle: {title}")
    links=extract_links(url,html)
    for link in links:
      if link not in visited:
        queue.append(link)
    print(f"\nVisited: {len(visited)} pages")
    
if __name__=="__main__":
  crawl("https://github.com/SxxAq", max_pages=10)
    
    
    
    