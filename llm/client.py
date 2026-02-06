"""
Google Gemini client - handles all LLM calls
Supports structured JSON outputs using Pydantic models
"""
import os
import json
from typing import Any, Dict, List, Optional
from google import genai
from google.genai import types
from pydantic import BaseModel


class LLMClient:
    """Wraps the Gemini API - makes it easy to get structured JSON responses"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "models/gemini-flash-latest"  # Using the free tier model
    
    def generate_structured_output(
        self,
        prompt: str,
        system_prompt: str,
        response_format: Optional[type[BaseModel]] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Main method for getting structured JSON from the LLM
        Pass in a Pydantic model and it'll return data matching that schema
        """
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Add JSON schema to the prompt if we want structured output
            if response_format:
                schema = response_format.model_json_schema()
                full_prompt += f"\n\nYou MUST respond with valid JSON matching this schema:\n{json.dumps(schema, indent=2)}"
                full_prompt += "\n\nRespond ONLY with the JSON object, no additional text."
            
            # Call Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                )
            )
            
            response_text = response.text.strip()
            
            # Sometimes Gemini wraps JSON in markdown code blocks, so clean that up
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse the JSON
            try:
                result = json.loads(response_text)
                
                # Validate it matches our Pydantic model if we have one
                if response_format:
                    validated = response_format(**result)
                    return validated.model_dump()
                
                return result
            except json.JSONDecodeError as e:
                # Fallback: try to extract JSON from the text using regex
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    if response_format:
                        validated = response_format(**result)
                        return validated.model_dump()
                    return result
                raise Exception(f"Failed to parse JSON response: {str(e)}\nResponse: {response_text[:200]}")
                
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
    
    def generate_text(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful AI assistant.",
        temperature: float = 0.7
    ) -> str:
        """Simple text generation - no structured output"""
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                )
            )
            
            return response.text
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")

