from typing import Dict, Any
from .schemas import Product

def normalize_product(raw: Dict[str, Any]) -> Product:
    """
    Normalize a raw product dictionary from Qdrant into a Product model.
    Ensures all required fields are present and optional fields have fallbacks.
    """
    # Ensure required fields are present
    if not all(k in raw for k in ["id", "title", "price"]):
        raise ValueError("Product missing required fields: id, title, or price")
    
    # Convert price to float if it's a string
    price = float(raw["price"]) if isinstance(raw["price"], str) else raw["price"]
    
    return Product(
        id=raw["id"],
        title=raw["title"],
        price=price,
        description=raw.get("description", "No description available"),
        image_url=raw.get("image_url", ""),
        tier=raw.get("tier", "unspecified"),
        category=raw.get("category", "uncategorized"),
        variant_id=raw.get("variant_id")
    )
