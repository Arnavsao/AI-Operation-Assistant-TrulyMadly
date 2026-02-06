"""
News API Tool for fetching latest news articles
"""
import os
import requests
from typing import Any, Dict, Optional
from .base import BaseTool


class NewsTool(BaseTool):
    """Tool for fetching news articles"""
    
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        if not self.api_key:
            raise ValueError("NEWS_API_KEY environment variable is required")
        self.base_url = "https://newsapi.org/v2"
    
    @property
    def name(self) -> str:
        return "get_news"
    
    @property
    def description(self) -> str:
        return "Get latest news articles on a specific topic or from a category"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for news articles (e.g., 'artificial intelligence', 'climate change')"
                },
                "category": {
                    "type": "string",
                    "description": "News category: business, technology, sports, entertainment, health, science",
                    "enum": ["business", "technology", "sports", "entertainment", "health", "science"]
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of articles to return (1-10)",
                    "default": 5
                }
            }
        }
    
    def execute(self, query: Optional[str] = None, category: Optional[str] = None, limit: int = 5) -> Dict[str, Any]:
        """
        Get news articles
        
        Args:
            query: Search query (optional)
            category: News category (optional)
            limit: Number of articles
            
        Returns:
            Dictionary with success status and news data
        """
        try:
            # Validate limit
            limit = max(1, min(10, limit))
            
            # Determine endpoint and parameters
            if query:
                url = f"{self.base_url}/everything"
                params = {
                    "q": query,
                    "apiKey": self.api_key,
                    "pageSize": limit,
                    "sortBy": "publishedAt",
                    "language": "en"
                }
            elif category:
                url = f"{self.base_url}/top-headlines"
                params = {
                    "category": category,
                    "apiKey": self.api_key,
                    "pageSize": limit,
                    "language": "en"
                }
            else:
                # Default to top headlines
                url = f"{self.base_url}/top-headlines"
                params = {
                    "apiKey": self.api_key,
                    "pageSize": limit,
                    "language": "en",
                    "country": "us"
                }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article["title"],
                    "description": article.get("description", ""),
                    "source": article["source"]["name"],
                    "author": article.get("author", "Unknown"),
                    "published_at": article["publishedAt"],
                    "url": article["url"]
                })
            
            return {
                "success": True,
                "data": {
                    "total_results": data.get("totalResults", 0),
                    "articles": articles
                }
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"News API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
