from readability import Document
from bs4 import BeautifulSoup

def extract_content(html:str)->str:
    """Extract the main content from an HTML page using Readability."""
    try:
        doc = Document(html)
        content_html = doc.summary()
        soup = BeautifulSoup(content_html, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        print(f"Error extracting content: {e}")
        return ""