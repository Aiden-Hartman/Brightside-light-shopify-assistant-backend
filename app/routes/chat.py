from fastapi import APIRouter, Request, Depends
from ..models.schemas import ChatRequest, ChatResponse
from ..services.gpt_service import gpt_service
from ..utils import validate_api_key, check_rate_limit

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: Request,
    chat_request: ChatRequest,
    _: None = Depends(validate_api_key)
) -> ChatResponse:
    """
    Chat endpoint that uses GPT to answer questions about products.
    """
    # Check rate limit
    check_rate_limit(request.client.host, request)
    
    # Get response from GPT service
    reply = await gpt_service.ask_about_products(
        message=chat_request.message,
        context=chat_request.context
    )
    
    return ChatResponse(reply=reply)
