from typing import Dict, List, Optional, TypedDict
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str
    title: str
    price: float
    description: Optional[str] = "No description available"
    image_url: Optional[str] = ""
    tier: Optional[str] = "unspecified"
    category: Optional[str] = "uncategorized"

class QuizAnswer(BaseModel):
    question: str
    answer: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatContext(TypedDict, total=False):
    products: List[Product]
    answers: List[QuizAnswer]
    summary: str
    chatMessages: List[ChatMessage]

class ChatRequest(BaseModel):
    message: str
    context: ChatContext = Field(
        default_factory=lambda: {
            "products": [],
            "summary": "",
            "chatMessages": []
        }
    )

class ChatResponse(BaseModel):
    reply: str

class SearchRequest(BaseModel):
    filters: Optional[Dict[str, str]] = None
    limit: Optional[int] = Field(default=10, ge=1, le=100)

class SearchResponse(BaseModel):
    products: List[Product]
