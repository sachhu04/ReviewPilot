from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AIProvider(ABC):
    """
    Base class for AI Providers.
    All providers (Groq, OpenAI, Anthropic, etc.) must implement this interface.
    """
    
    @abstractmethod
    def generate_review(self, prompt: str, system_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Takes an optimized prompt and returns a structured JSON review dict.
        """
        pass
