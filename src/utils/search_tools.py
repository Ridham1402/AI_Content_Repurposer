from tavily import TavilyClient
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class SearchTools:
    """Unified search interface using multiple sources"""
    
    def __init__(self):
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    def tavily_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search using Tavily (LLM-optimized, returns clean content)
        """
        try:
            response = self.tavily_client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced"  # More comprehensive results
            )
            
            results = []
            for item in response.get('results', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('content', ''),
                    'score': item.get('score', 0)
                })
            
            return results
        except Exception as e:
            print(f"Tavily search error: {e}")
            return []
    
    def duckduckgo_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Backup search using DuckDuckGo (free, unlimited)
        """
        try:
            ddgs = DDGS()
            results = []
            
            for result in ddgs.text(query, max_results=max_results):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'content': result.get('body', ''),
                    'score': 1.0  # DDG doesn't provide scores
                })
            
            return results
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return []
    
    def smart_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Intelligently uses Tavily first, falls back to DuckDuckGo
        """
        # Try Tavily first (better for LLM consumption)
        results = self.tavily_search(query, max_results)
        
        # Fallback to DuckDuckGo if Tavily fails or returns nothing
        if not results:
            print("Tavily failed, using DuckDuckGo backup...")
            results = self.duckduckgo_search(query, max_results)
        
        return results
