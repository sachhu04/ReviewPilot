import json
import time
from typing import Dict, Any, Optional
from groq import Groq
from config.settings import settings
from providers.base import AIProvider

class GroqProvider(AIProvider):
    def __init__(self):
        # Instantiate Groq client using the API key from settings.
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        # Using LLaMA 3 or mixtral model which supports JSON mode
        self.model = "llama3-70b-8192"

    def generate_review(self, prompt: str, system_message: Optional[str] = None) -> Dict[str, Any]:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        retries = 3
        for attempt in range(retries):
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model=self.model,
                    response_format={"type": "json_object"},
                    temperature=0.2, # Low temperature for more deterministic, analytical responses
                    max_tokens=4000
                )
                
                content = chat_completion.choices[0].message.content
                if not content:
                    raise ValueError("Empty response received from Groq")
                    
                parsed_json = json.loads(content)
                return parsed_json
            except Exception as e:
                if attempt == retries - 1:
                    # Log error in real app
                    raise Exception(f"Failed to generate review after {retries} attempts: {str(e)}")
                time.sleep(1.5 ** attempt) # Exponential backoff
