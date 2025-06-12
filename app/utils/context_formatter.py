from typing import List, Dict
from ..models.schemas import Product, QuizAnswer, ChatMessage

def format_context_to_system_prompt(context: Dict) -> str:
    """
    Formats the context information into a comprehensive system prompt for GPT.
    
    Args:
        context: Dictionary containing products, answers, summary, and chat messages
        
    Returns:
        str: Formatted system prompt
    """
    products = context.get("products", [])
    answers = context.get("answers", [])
    summary = context.get("summary", "")
    chat_messages = context.get("chatMessages", [])
    
    # Format products section
    products_section = "Current Selected Products:\n"
    for product in products:
        products_section += f"- {product['title']} (${product['price']:.2f})\n"
        if product.get('description'):
            products_section += f"  Description: {product['description']}\n"
        products_section += f"  Category: {product.get('category', 'uncategorized')}, Tier: {product.get('tier', 'unspecified')}\n\n"
    
    # Format summary section
    summary_section = f"Product Summary:\n{summary}\n\n" if summary else ""
    
    # Format chat history section
    chat_history = "Recent Chat History:\n"
    for msg in chat_messages[-5:]:  # Only include last 5 messages for context
        chat_history += f"{msg.role}: {msg.content}\n"
    
    # Combine all sections into the final system prompt
    system_prompt = f"""You are an AI assistant for Brightside, a supplement company. 
Your role is to help customers understand our products and their benefits.

Guidelines:
- Be professional but conversational
- Focus on explaining products, ingredients, and use cases
- DO NOT give medical advice
- Keep answers clear and concise
- Use accessible language, avoid technical jargon
- If unsure about something, say so rather than making assumptions

{products_section}
{summary_section}
{chat_history}

Please use the above context to provide informed and personalized responses to the user's questions."""
    
    return system_prompt 