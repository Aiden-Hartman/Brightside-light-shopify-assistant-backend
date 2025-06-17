from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Literal
import logging
from ..services.gpt_service import gpt_service
from ..utils.api_utils import validate_api_key

router = APIRouter()
logger = logging.getLogger(__name__)

# Request and response schemas
class ClassifyProduct(BaseModel):
    title: str
    description: str

class ClassifyRequest(BaseModel):
    message: str
    products: List[ClassifyProduct]

class ClassifyResponse(BaseModel):
    status: Literal['ok', 'fallback']
    required_context: List[str]

@router.post("/classify", response_model=ClassifyResponse)
async def classify(
    request: Request,
    classify_request: ClassifyRequest,
    _: None = Depends(validate_api_key)
) -> ClassifyResponse:
    """
    Classify endpoint that uses GPT to determine which products are relevant to the user's question.
    """
    logger.info("="*50)
    logger.info("🆕 New Classify Request Received")
    logger.info(f"🔗 Client IP: {request.client.host}")
    logger.info(f"📝 User Message: {classify_request.message}")
    logger.info(f"📦 Products: {[p.title for p in classify_request.products]}")
    # Build the classifier prompt
    products = classify_request.products
    message = classify_request.message
    prompt = (
        "You are a product classification assistant for a supplement company. Your job is to analyze user questions and determine which products (if any) are needed to answer them.\n\n"
        f"You have access to the following products:\n{chr(10).join([f'- {p.title}: {p.description}' for p in products])}\n\n"
        f"User question: \"{message}\"\n\n"
        "Your task:\n"
        "1. Analyze if the question is about our products/ingredients\n"
        "2. Determine if it's a medical/medication question\n"
        "3. Check if it's a general question not about our products\n"
        "4. Identify if it's a thank you or other non-product question\n\n"
        "Rules:\n"
        "- Only return product titles that EXACTLY match the ones provided above\n"
        "- If the question is about medications, health conditions, or medical advice, return fallback\n"
        "- If the question is not about our products, return fallback\n"
        "- If it's a thank you or general conversation, return fallback\n"
        "- For comparison questions, include all relevant products\n"
        "- For ingredient questions, include products containing those ingredients\n"
        "- For health benefit questions, include products that address those benefits\n\n"
        "Return your response in this exact JSON format:\n"
        "{\n  \"status\": \"ok\" | \"fallback\",\n  \"required_context\": [\"Product Title 1\", \"Product Title 2\"]\n}\n\n"
        "Examples:\n"
        "1. \"What product has calcium?\"\n   {\n     \"status\": \"ok\",\n     \"required_context\": [\"Bone Health Plus\"]\n   }\n"
        "2. \"Can I take this with my blood pressure meds?\"\n   {\n     \"status\": \"fallback\",\n     \"required_context\": []\n   }\n"
        "3. \"What's the difference between your brain supplements?\"\n   {\n     \"status\": \"ok\",\n     \"required_context\": [\"CogniAid™\", \"Brain Boost\"]\n   }\n"
        "4. \"Thank you for your help!\"\n   {\n     \"status\": \"fallback\",\n     \"required_context\": []\n   }\n"
        "5. \"Do you have anything for digestion?\"\n   {\n     \"status\": \"ok\",\n     \"required_context\": [\"GI Revive\"]\n   }\n\n"
        "Remember:\n"
        "- Be precise with product titles\n"
        "- Only include products that exist in the provided list\n"
        "- Return fallback for any medical advice questions\n"
        "- Return fallback for questions about products we don't have\n"
        "- Return fallback for general conversation\n\n"
        f"Now, classify this question: \"{message}\""
    )
    try:
        import json
        # Call GPT (reuse gpt_service)
        gpt_response = await gpt_service.client.chat.completions.create(
            model=gpt_service.model,
            messages=[
                {"role": "system", "content": prompt}
            ],
            temperature=0,
            max_tokens=300,
            timeout=10
        )
        raw_content = gpt_response.choices[0].message.content.strip()
        logger.info(f"🤖 GPT Raw Output: {raw_content}")
        parsed = json.loads(raw_content)
        status = parsed.get("status")
        required_context = parsed.get("required_context", [])
        if status not in ("ok", "fallback") or not isinstance(required_context, list):
            raise ValueError("Malformed response from GPT")
        logger.info(f"✅ Classify status: {status}, required_context: {required_context}")
        return ClassifyResponse(status=status, required_context=required_context)
    except Exception as e:
        logger.error(f"❌ Error processing classify request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing classify request: {str(e)}") 