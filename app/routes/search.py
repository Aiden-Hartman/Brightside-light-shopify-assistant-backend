from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from ..models.schemas import SearchRequest, SearchResponse
from ..services.qdrant_service import qdrant_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/search", response_model=SearchResponse)
async def search(
    request: Request,
    search_request: SearchRequest
) -> SearchResponse:
    """
    Search endpoint that returns product recommendations based on filters.
    """
    try:
        # Log request details
        logger.info("="*50)
        logger.info("🔍 New Search Request Received")
        logger.info(f"📝 Request ID: {id(request)}")
        logger.info(f"🔗 Client IP: {request.client.host}")
        logger.info(f"📦 Request Body: {search_request.dict()}")
        logger.info(f"🔍 Filters: {search_request.filters}")
        logger.info(f"📊 Limit: {search_request.limit}")
        
        # Query products from Qdrant
        logger.info("🔄 Querying Qdrant database...")
        products = qdrant_service.query_products_with_filters(
            filters=search_request.filters,
            limit=search_request.limit
        )
        
        # Log response details
        logger.info(f"✅ Query successful - Found {len(products)} products")
        if products:
            logger.info("📋 First product details:")
            first_product = products[0]
            logger.info(f"  - ID: {first_product.id}")
            logger.info(f"  - Title: {first_product.title}")
            logger.info(f"  - Price: {first_product.price}")
            logger.info(f"  - Category: {first_product.category}")
            logger.info(f"  - Tier: {first_product.tier}")
        
        logger.info("="*50)
        return SearchResponse(products=products)
    except Exception as e:
        logger.error("❌ Error processing search request")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}", exc_info=True)
        logger.error("="*50)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing search request: {str(e)}"
        )
