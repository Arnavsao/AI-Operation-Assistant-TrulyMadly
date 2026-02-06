"""
LLM Client for Google Gemini integration with structured outputs
"""
import os
import json
from typing import Any, Dict, List, Optional
from google import genai
from google.genai import types
from pydantic import BaseModel


class LLMClient:
    """Wrapper for Google Gemini API with structured output support"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "models/gemini-flash-latest"  # Latest free tier model with good quota
    
    def generate_structured_output(
        self,
        prompt: str,
        system_prompt: str,
        response_format: Optional[type[BaseModel]] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate structured output from LLM
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            response_format: Pydantic model for structured output
            temperature: Sampling temperature
            
        Returns:
            Parsed JSON response
        """
        try:
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # If we have a response format, add JSON schema instructions
            if response_format:
                schema = response_format.model_json_schema()
                full_prompt += f"\n\nYou MUST respond with valid JSON matching this schema:\n{json.dumps(schema, indent=2)}"
                full_prompt += "\n\nRespond ONLY with the JSON object, no additional text."
            
            # Generate response
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
            
            # Extract text
            response_text = response.text.strip()
            
            # Clean up markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            try:
                result = json.loads(response_text)
                
                # Validate against Pydantic model if provided
                if response_format:
                    validated = response_format(**result)
                    return validated.model_dump()
                
                return result
            except json.JSONDecodeError as e:
                # If JSON parsing fails, try to extract JSON from text
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
        """
        Generate plain text output from LLM
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
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
