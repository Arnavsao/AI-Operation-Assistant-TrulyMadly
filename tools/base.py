"""
Base tool interface for all API integrations
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Abstract base class for all tools"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for LLM"""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """Tool parameters schema"""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters
        
        Returns:
            Result dictionary with 'success' and 'data' or 'error' keys
        """
        pass
    
    def to_schema(self) -> Dict[str, Any]:
        """Convert tool to schema format for LLM"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
