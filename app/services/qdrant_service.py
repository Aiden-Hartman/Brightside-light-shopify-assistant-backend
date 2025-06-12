from typing import Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging
from fastapi import HTTPException

from ..config import get_settings
from ..models.schemas import Product
from ..models.product_model import normalize_product

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        settings = get_settings()
        try:
            print("Initializing Qdrant client")
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key
            )
            self.collection_name = settings.qdrant_collection
            
            # Verify collection exists
            try:
                collections = self.client.get_collections().collections
                collection_names = [collection.name for collection in collections]
                print("="*50)
                print("📚 Available Collections")
                print(f"Found {len(collection_names)} collections:")
                for name in collection_names:
                    print(f"  - {name}")
                print(f"Using collection: {self.collection_name}")
                
                if self.collection_name not in collection_names:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Collection {self.collection_name} not found in Qdrant"
                    )
                    
                # Try to get a sample point to verify collection is accessible
                try:
                    points, _ = self.client.scroll(
                        collection_name=self.collection_name,
                        limit=1,
                        with_payload=True
                    )
                    if points and len(points) > 0:
                        print("\n✅ Successfully connected to collection")
                        print(f"Sample point ID: {points[0].id}")
                    else:
                        print("\n⚠️ Collection is empty")
                except Exception as e:
                    logger.warning(f"Could not fetch sample point: {str(e)}")
                    print("\n⚠️ Could not fetch sample point, but collection exists")
                
                print("="*50)
                
            except Exception as e:
                logger.error(f"Failed to verify collection: {str(e)}", exc_info=True)
                raise HTTPException(
                    status_code=500,
                    detail="Failed to connect to search service"
                )
                
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Failed to initialize search service"
            )

    def query_products_with_filters(
        self,
        filters: Optional[Dict[str, str]] = None,
        limit: int = 10
    ) -> List[Product]:
        """
        Query products from Qdrant using metadata filters.
        Returns normalized Product objects.
        """
        print("="*50)
        print("Querying products with filters")
        print(f"Filters: {filters}")
        print(f"Limit: {limit}")
        print("="*50)

        if not filters:
            print("No filters provided")
            filters = {}

        try:
            # Get all points and filter in memory
            points, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=1000,  # Get a reasonable number of points
                with_payload=True
            )
            
            # Filter points based on criteria
            filtered_points = []
            for point in points:
                matches = True
                for key, value in filters.items():
                    if key not in point.payload or point.payload[key] != value:
                        matches = False
                        break
                if matches:
                    filtered_points.append(point)
                    
            # Take only the requested number of points
            results = filtered_points[:limit]

            # Normalize and return products
            return [
                normalize_product(point.payload)
                for point in results
            ]
        except Exception as e:
            logger.error(f"Error querying Qdrant: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Error querying product database"
            )

# Create a singleton instance
qdrant_service = QdrantService()
