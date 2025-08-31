from fastapi import FastAPI, HTTPException
from .routers import items
from .core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="A simple FastAPI example for GitHub Actions course",
    version="1.0.0"
)

# Include routers
app.include_router(items.router, prefix="/api/v1", tags=["items"])

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message"""
    return {"message": f"Welcome to {settings.app_name}!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.get("/api/v1/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get item by ID"""
    item = await items.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item