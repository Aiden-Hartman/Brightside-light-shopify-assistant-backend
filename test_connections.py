import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
import socket

# Load environment variables
load_dotenv()

async def test_openai():
    """Test OpenAI connection"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("GPT_MODEL")
        print(f"[DEBUG] OPENAI_API_KEY starts with: {api_key[:8] if api_key else None}")
        print(f"[DEBUG] GPT_MODEL: {model}")
        client = AsyncOpenAI(api_key=api_key)
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello!"}],
            max_tokens=5
        )
        print("✅ OpenAI connection successful!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print("❌ OpenAI connection failed!")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

def test_qdrant():
    """Test Qdrant connection"""
    try:
        qdrant_url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")
        print(f"[DEBUG] QDRANT_URL: {qdrant_url}")
        print(f"[DEBUG] QDRANT_API_KEY starts with: {api_key[:8] if api_key else None}")
        if qdrant_url:
            try:
                host = qdrant_url.split('//')[-1].split('/')[0]
                print(f"[DEBUG] Qdrant host: {host}")
                print(f"[DEBUG] Attempting DNS resolution for host: {host}")
                print(f"[DEBUG] Resolved IPs: {socket.gethostbyname_ex(host)}")
            except Exception as dns_e:
                print(f"[DEBUG] DNS resolution failed: {dns_e}")
        if not qdrant_url or not qdrant_url.startswith("https://"):
            print("⚠️ Warning: Qdrant Cloud URL should start with 'https://'")
        print(f"Attempting to connect to Qdrant Cloud at: {qdrant_url}")
        client = QdrantClient(
            url=qdrant_url,
            api_key=api_key
        )
        # Try to get collections
        collections = client.get_collections()
        print("✅ Qdrant Cloud connection successful!")
        print(f"Available collections: {[c.name for c in collections.collections]}")
    except Exception as e:
        print("❌ Qdrant Cloud connection failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting tips for Qdrant Cloud:")
        print("1. Verify your API key is correct and active")
        print("2. Check if your instance is running in the Qdrant Cloud dashboard")
        print("3. Ensure your IP is whitelisted if you have IP restrictions enabled")
        print("4. Verify the URL format is correct (should be https://your-instance.cloud.qdrant.io)")

async def main():
    print("Testing API connections...\n")
    print("\nTesting Qdrant...")
    test_qdrant()

if __name__ == "__main__":
    asyncio.run(main()) 