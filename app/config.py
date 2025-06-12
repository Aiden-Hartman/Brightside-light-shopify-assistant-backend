import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

class Settings:
    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    gpt_model: str = os.getenv("GPT_MODEL", "gpt-3.5-turbo")
    
    # Qdrant settings
    qdrant_url: str = os.getenv("QDRANT_URL")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION")
    
    # API key settings
    require_api_key: bool = os.getenv("REQUIRE_API_KEY", "").lower() == "true"
    expected_api_key: Optional[str] = os.getenv("EXPECTED_API_KEY")
    
    # Rate limiting
    rate_limit_per_hour: int = int(os.getenv("RATE_LIMIT_PER_HOUR", "20"))

@lru_cache()
def get_settings() -> Settings:
    return Settings()
