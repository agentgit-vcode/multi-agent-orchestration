"""
LLM Handler for OpenAI and Google Gemini Integration
Handles all interactions with the LLM APIs
"""

import os
import time
from typing import Optional, Dict, Any, List
import logging
from dotenv import load_dotenv

from metrics import LLMCallMetrics

# Load environment variables from .env file
load_dotenv(override=True)

logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not installed. Install with: pip install openai")

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logger.warning("Google Generative AI library not installed. Install with: pip install google-generativeai")


class LLMHandler:
    """Handles LLM calls using OpenAI or Google Gemini API"""

    def __init__(self, provider: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the LLM client.

        Args:
            provider: Override LLM provider ('openai' or 'google'). Defaults to LLM_PROVIDER env var.
            model_name: Override model name. Defaults to provider-specific env var.
        """
        self.llm_provider = (provider or os.getenv('LLM_PROVIDER', 'openai')).lower()

        if self.llm_provider == 'google':
            if not GOOGLE_AVAILABLE:
                raise ImportError("Google Generative AI library not installed. Run: pip install google-generativeai")

            self.google_api_key = os.getenv('GOOGLE_API_KEY')
            if not self.google_api_key:
                raise ValueError(
                    "GOOGLE_API_KEY not found in environment variables. "
                    "Create a .env file with: GOOGLE_API_KEY=your-key-here"
                )

            genai.configure(api_key=self.google_api_key)
            self.model_name = model_name or os.getenv('GOOGLE_MODEL', 'gemini-pro-latest')
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"LLM Handler initialized with Google Gemini model: {self.model_name}")

        elif self.llm_provider == 'openai':
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI library not installed. Run: pip install openai")

            self.openai_api_key = os.getenv('OPENAI_API_KEY')
            if not self.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY not found in environment variables. "
                    "Create a .env file with: OPENAI_API_KEY=your-key-here"
                )

            self.client = OpenAI(api_key=self.openai_api_key)
            self.model_name = model_name or os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
            self.temperature = float(os.getenv('OPENAI_TEMPERATURE', 0.7))
            logger.info(f"LLM Handler initialized with OpenAI model: {self.model_name}")

        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}. Supported providers are 'openai' and 'google'.")

    def call(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1000,
             agent_name: str = 'unknown') -> Dict[str, Any]:
        """
        Make a call to the LLM API.

        Args:
            prompt: The user/main prompt
            system_prompt: Optional system prompt to set behavior
            max_tokens: Maximum tokens in response
            agent_name: Name of the calling agent (for metrics)

        Returns:
            Dict with 'text' (response string) and 'metrics' (LLMCallMetrics)
        """
        start_time = time.time()

        try:
            if self.llm_provider == 'google':
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                response = self.model.generate_content(full_prompt)
                result = response.text
                duration = time.time() - start_time

                # Estimate tokens for Gemini (no exact counts from API)
                prompt_tokens = len(full_prompt) // 4
                completion_tokens = len(result) // 4

                metrics = LLMCallMetrics(
                    agent_name=agent_name,
                    provider='google',
                    model=self.model_name,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                    duration_seconds=round(duration, 2),
                    tokens_estimated=True,
                )
                logger.info(f"Google Gemini call successful. ~{metrics.total_tokens} tokens (est), {duration:.2f}s")
                return {'text': result, 'metrics': metrics}

            elif self.llm_provider == 'openai':
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=max_tokens
                )

                result = response.choices[0].message.content
                duration = time.time() - start_time

                prompt_tokens = response.usage.prompt_tokens if response.usage else 0
                completion_tokens = response.usage.completion_tokens if response.usage else 0
                total_tokens = response.usage.total_tokens if response.usage else 0

                metrics = LLMCallMetrics(
                    agent_name=agent_name,
                    provider='openai',
                    model=self.model_name,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    duration_seconds=round(duration, 2),
                    tokens_estimated=False,
                )
                logger.info(f"OpenAI call successful. {total_tokens} tokens, {duration:.2f}s")
                return {'text': result, 'metrics': metrics}

        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            raise

    @staticmethod
    def get_available_models() -> List[Dict[str, str]]:
        """Return list of available provider/model combinations based on configured API keys."""
        models = []

        if GOOGLE_AVAILABLE and os.getenv('GOOGLE_API_KEY'):
            models.append({'provider': 'google', 'model': os.getenv('GOOGLE_MODEL', 'gemini-pro-latest'),
                           'label': 'Google Gemini'})

        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            models.append({'provider': 'openai', 'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
                           'label': 'OpenAI GPT'})

        return models


# Create a global LLM handler instance (lazy loaded)
_llm_handler: Optional[LLMHandler] = None


def get_llm_handler() -> LLMHandler:
    """Get the global LLM handler instance"""
    global _llm_handler

    if _llm_handler is None:
        _llm_handler = LLMHandler()

    return _llm_handler


def is_llm_available() -> bool:
    """Check if LLM is available"""
    if os.getenv('LLM_PROVIDER', 'openai').lower() == 'google':
        return GOOGLE_AVAILABLE and os.getenv('GOOGLE_API_KEY') is not None
    else:
        return OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY') is not None
