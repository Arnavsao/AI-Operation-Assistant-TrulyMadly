"""
GitHub API Tool for repository search and information retrieval
"""
import os
import requests
from typing import Any, Dict, Optional
from .base import BaseTool


class GitHubTool(BaseTool):
    """Tool for interacting with GitHub API"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    @property
    def name(self) -> str:
        return "github_search"
    
    @property
    def description(self) -> str:
        return "Search GitHub repositories and get repository information including stars, forks, and description"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for repositories (e.g., 'machine learning python')"
                },
                "sort": {
                    "type": "string",
                    "description": "Sort by: stars, forks, updated",
                    "enum": ["stars", "forks", "updated"],
                    "default": "stars"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return (1-10)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    
    def execute(self, query: str, sort: str = "stars", limit: int = 5) -> Dict[str, Any]:
        """
        Search GitHub repositories
        
        Args:
            query: Search query
            sort: Sort criterion
            limit: Number of results
            
        Returns:
            Dictionary with success status and repository data
        """
        try:
            # Validate limit
            limit = max(1, min(10, limit))
            
            # Make API request
            url = f"{self.base_url}/search/repositories"
            params = {
                "q": query,
                "sort": sort,
                "order": "desc",
                "per_page": limit
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            repositories = []
            for repo in data.get("items", []):
                repositories.append({
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "description": repo["description"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "language": repo["language"],
                    "url": repo["html_url"],
                    "updated_at": repo["updated_at"]
                })
            
            return {
                "success": True,
                "data": {
                    "total_count": data.get("total_count", 0),
                    "repositories": repositories
                }
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"GitHub API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
