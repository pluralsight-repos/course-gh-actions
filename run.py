import uvicorn
from app.main import app
from app.core.config import get_settings
from app.core.logging import get_logger

if __name__ == "__main__":
    settings = get_settings()
    logger = get_logger("fastapi_app.startup")
    
    logger.info(f"Starting {settings.app_name} server")
    logger.info(f"Server will run on {settings.host}:{settings.port}")
    logger.info(f"Debug mode: {settings.debug}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_config=None  # Use our custom logging configuration
    )
