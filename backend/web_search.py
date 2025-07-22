from typing import List, Optional
from pydantic import BaseModel, Field
from googlesearch import search
from httpx import Client
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class SearchResult(BaseModel):
    url: str = Field(..., description="URL of the search result")

class SearchList(BaseModel):
    results: List[SearchResult] = Field(..., description="Search results")

class WebSearchTool:
    def __init__(
        self,
        language: Optional[str] = "en",
        timeout: Optional[int] = 1,
        sleep_interval: Optional[int] = 1,
    ):
        self.language = language
        self.timeout = timeout
        self.sleep_interval = sleep_interval

    def _validate_url(self, url: str) -> str:
        """Validate and fix URL format"""
        if not url:
            return None
            
        # Parse the URL
        parsed = urlparse(url)
        
        # If no scheme is provided, assume https
        if not parsed.scheme:
            url = f"https://{url}"
            parsed = urlparse(url)
        
        # Check if it's a valid HTTP/HTTPS URL
        if parsed.scheme not in ['http', 'https']:
            return None
            
        # Check if domain exists
        if not parsed.netloc:
            return None
            
        return url

    def web_search(
        self,
        query: str,
        max_results: int = 1,
        unique: bool = False,
    ) -> SearchList:
        result_list = []
        try:
            results = search(
                term=query,
                num_results=max_results,
                lang=self.language,
                start_num=0,
                unique=unique,
                sleep_interval=self.sleep_interval,
            )
            for _, result in enumerate(results):
                validated_url = self._validate_url(result)
                if validated_url:  # Only add valid URLs
                    result_list.append(SearchResult(url=validated_url))
        except Exception as e:
            # If search fails, return empty results
            print(f"Search failed for query '{query}': {str(e)}")

        return SearchList(results=result_list)

    def web_scrap(self, url: str) -> str:
        # Validate URL first
        validated_url = self._validate_url(url)
        if not validated_url:
            return f'Invalid URL format: {url}'
            
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
         }
        
        try:
            with Client(headers=headers) as client:
                response = client.get(validated_url, timeout=10)
                if response.status_code != 200:
                    return f'Failed to fetch {validated_url}. Code: {response.status_code}'

                soup = BeautifulSoup(response.text, 'html.parser')
                return soup.get_text().replace('\n', '').replace('\r', '')
        except Exception as e:
            return f'Error scraping {validated_url}: {str(e)}'

def test_web_search():
    tool = WebSearchTool()
    results = tool.web_search("wikipedia", max_results=1)
    print(results.results[0].url)
    assert isinstance(results, SearchList)
    assert len(results.results) == 1
    assert isinstance(results.results[0], SearchResult)
    assert results.results[0].url.startswith("https://")

def test_web_scrap():
    tool = WebSearchTool()
    url = "https://www.wikipedia.org/"
    content = tool.web_scrap(url)

    assert isinstance(content, str)
    assert "Wikipedia" in content 