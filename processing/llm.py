# processing/llm.py
import logging
from openai import OpenAI
import os

from config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    SYSTEM_PROMPT
)

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProcessor:
    """Handles interaction with OpenAI's API for generating responses."""
    
    def __init__(self, system_prompt=SYSTEM_PROMPT):
        """Initialize the LLM processor with API key and system prompt."""
        self.client = self._initialize_client()
        self.system_prompt = system_prompt
        self.conversation_history = [{"role": "system", "content": system_prompt}]
        logger.info("LLM processor initialized")
    
    def _initialize_client(self):
        """Create and return an OpenAI client instance."""
        try:
            return OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
    
    def add_message(self, message, role="user"):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": message
        })
    
    def get_response(self, user_input=None):
        """
        Generate a response using the OpenAI API.
        
        Args:
            user_input (str, optional): New user input to process
            
        Returns:
            str: The generated response text
        """
        if user_input:
            self.add_message(user_input, role="user")
        
        try:
            logger.info("Sending request to OpenAI")
            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=self.conversation_history,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            
            response_text = response.choices[0].message.content
            logger.info(f"Received response: {response_text[:50]}...")
            
            # Add response to conversation history
            self.add_message(response_text, role="assistant")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I had trouble processing your request. Could you try again?"
    
    def clear_history(self):
        """Reset the conversation history, keeping only the system prompt."""
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        logger.info("Conversation history cleared")

# Convenience function for simple use cases
def generate_response(user_input, conversation_history=None):
    """
    Generate a single response without managing conversation state.
    
    Args:
        user_input (str): The user's input
        conversation_history (list, optional): Previous conversation messages
        
    Returns:
        str: The generated response
    """
    processor = LLMProcessor()
    
    if conversation_history:
        processor.conversation_history = conversation_history
    
    return processor.get_response(user_input)