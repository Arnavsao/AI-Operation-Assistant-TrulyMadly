"""
OpenWeatherMap API Tool for weather information
"""
import os
import requests
from typing import Any, Dict
from .base import BaseTool


class WeatherTool(BaseTool):
    """Tool for fetching weather information"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable is required")
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    @property
    def name(self) -> str:
        return "get_weather"
    
    @property
    def description(self) -> str:
        return "Get current weather information for a city including temperature, conditions, humidity, and wind speed"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name (e.g., 'London', 'New York', 'Mumbai')"
                },
                "units": {
                    "type": "string",
                    "description": "Temperature units: metric (Celsius) or imperial (Fahrenheit)",
                    "enum": ["metric", "imperial"],
                    "default": "metric"
                }
            },
            "required": ["city"]
        }
    
    def execute(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Get current weather for a city
        
        Args:
            city: City name
            units: Temperature units (metric or imperial)
            
        Returns:
            Dictionary with success status and weather data
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            weather_info = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "conditions": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "units": "°C" if units == "metric" else "°F"
            }
            
            return {
                "success": True,
                "data": weather_info
            }
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return {
                    "success": False,
                    "error": f"City '{city}' not found"
                }
            return {
                "success": False,
                "error": f"Weather API request failed: {str(e)}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Weather API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
