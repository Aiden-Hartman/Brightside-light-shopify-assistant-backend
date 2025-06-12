from typing import List, Dict
import openai
from ..config import get_settings
from ..models.schemas import Product
from ..utils.context_formatter import format_context_to_system_prompt

class GPTService:
    def __init__(self):
        settings = get_settings()
        self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.gpt_model

    async def ask_about_products(self, message: str, context: Dict) -> str:
        """
        Generate a response about products using GPT with full context.
        
        Args:
            message: The user's message
            context: Dictionary containing products, answers, summary, and chat messages
        """
        # Format the context into a system prompt
        system_prompt = format_context_to_system_prompt(context)

        # Prepare the messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please respond to this message using the context above: {message}"}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Log the error in production
            raise Exception(f"Error calling OpenAI API: {str(e)}")

# Create a singleton instance
gpt_service = GPTService()
