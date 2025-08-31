from fastapi import FastAPI, HTTPException
from .routers import items
from .core.config import get_settings
from .core.logging import setup_logging, get_logger
from .middleware import LoggingMiddleware

# Get settings
settings = get_settings()

# Setup logging
setup_logging(
    log_level=settings.log_level,
    log_format=settings.log_format,
    log_file=settings.log_file if settings.enable_file_logging else None,
    enable_json_logs=settings.enable_json_logs
)

# Get logger
logger = get_logger("fastapi_app.main")

# Log application startup
logger.info(f"Starting {settings.app_name} application")
logger.info(f"Debug mode: {settings.debug}")
logger.info(f"Log level: {settings.log_level}")

app = FastAPI(
    title=settings.app_name,
    description="A simple FastAPI example for GitHub Actions course",
    version="1.0.0"
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(items.router, prefix="/api/v1", tags=["items"])
logger.info("Registered items router at /api/v1")

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message"""
    logger.info("Root endpoint accessed")
    return {"message": f"Welcome to {settings.app_name}!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check endpoint accessed")
    return {"status": "healthy", "message": "API is running"}

# Application lifecycle events
@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application shutdown")