from datetime import datetime, timedelta
from typing import Dict, Tuple
from fastapi import HTTPException, Request
from ..config import get_settings

# Simple in-memory rate limiter
_rate_limits: Dict[str, Tuple[int, datetime]] = {}

def validate_api_key(request: Request) -> None:
    """Temporarily disabled API key validation for debugging CORS issues."""
    return

def check_rate_limit(ip: str, request: Request = None) -> None:
    """Temporarily disabled rate limiting for debugging CORS issues."""
    return 