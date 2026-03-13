"""
LLM Handler for OpenAI Integration
Handles all interactions with the OpenAI API
"""

import os
from typing import Optional
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not installed. Install with: pip install openai")


class LLMHandler:
    """Handles LLM calls using OpenAI API"""
    
    def __init__(self):
        """Initialize the OpenAI client"""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
        
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Create a .env file with: OPENAI_API_KEY=your-key-here"
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', 0.7))
        
        logger.info(f"LLM Handler initialized with model: {self.model}")
    
    def call(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1000) -> str:
        """
        Make a call to the OpenAI API
        
        Args:
            prompt: The user/main prompt
            system_prompt: Optional system prompt to set behavior
            max_tokens: Maximum tokens in response
        
        Returns:
            The LLM response text
        """
        try:
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add user prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=max_tokens
            )
            
            # Extract and return the response
            result = response.choices[0].message.content
            logger.info(f"LLM call successful. Tokens used: {response.usage.total_tokens}")
            return result
        
        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            raise
    
    def plan(self, query: str) -> str:
        """Generate a plan for a query"""
        system_prompt = """You are an expert planner. Your task is to create a clear, structured plan 
        to address the given query. Break it down into logical steps."""
        
        prompt = f"Create a detailed plan for: {query}"
        return self.call(prompt, system_prompt, max_tokens=1000)
    
    def research(self, query: str, context: str = "") -> str:
        """Research information about a topic"""
        system_prompt = """You are an expert researcher. Provide comprehensive, well-researched 
        information about the given topic. Include key facts, sources, and important details."""
        
        prompt = f"Research and provide detailed information about: {query}"
        if context:
            prompt += f"\n\nContext: {context}"
        
        return self.call(prompt, system_prompt, max_tokens=1500)
    
    def analyze(self, query: str, research_data: str) -> str:
        """Analyze research data"""
        system_prompt = """You are an expert analyst. Analyze the provided information and 
        identify key insights, patterns, and actionable conclusions."""
        
        prompt = f"""Analyze the following research data about '{query}':

{research_data}

Provide key findings, patterns, and insights."""
        
        return self.call(prompt, system_prompt, max_tokens=1200)
    
    def publish(self, query: str, plan: str, research: str, analysis: str) -> str:
        """Create a final comprehensive report"""
        system_prompt = """You are an expert report writer. Create a comprehensive, 
        well-structured report that synthesizes all the provided information."""
        
        prompt = f"""Create a final comprehensive report for the query: {query}

Using the following information:

PLAN:
{plan}

RESEARCH:
{research}

ANALYSIS:
{analysis}

Create a well-structured final report that synthesizes all this information."""
        
        return self.call(prompt, system_prompt, max_tokens=2000)


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
    return OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY') is not None
