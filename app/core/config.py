from functools import lru_cache
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "Simple FastAPI"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "detailed"  # simple, detailed, json
    log_file: str = "logs/app.log"
    enable_json_logs: bool = False
    enable_file_logging: bool = True

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
