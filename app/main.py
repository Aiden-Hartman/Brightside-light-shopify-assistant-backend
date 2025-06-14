from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chat, search

app = FastAPI(
    title="Brightside API",
    description="API for Brightside supplement recommendations and chat",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://brightside-light-shopify-assistant.vercel.app",
    "https://brightside-light-frontend-v2.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
