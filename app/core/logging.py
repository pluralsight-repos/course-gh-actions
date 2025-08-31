import logging
import logging.config
import sys
from pathlib import Path
from typing import Dict, Any
import json
from datetime import datetime


class CustomFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to levelname for console output
        if hasattr(record, 'color') and record.color:
            color = self.COLORS.get(record.levelname, '')
            record.levelname = f"{color}{record.levelname}{self.RESET}"
        
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'endpoint'):
            log_entry['endpoint'] = record.endpoint
        if hasattr(record, 'method'):
            log_entry['method'] = record.method
        if hasattr(record, 'status_code'):
            log_entry['status_code'] = record.status_code
        if hasattr(record, 'duration'):
            log_entry['duration'] = record.duration
            
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry)


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "detailed",
    log_file: str = None,
    enable_json_logs: bool = False
) -> None:
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Format style ('simple', 'detailed', 'json')
        log_file: Path to log file (if None, only console logging)
        enable_json_logs: Whether to enable JSON formatted logs
    """
    
    # Ensure logs directory exists
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Define formatters
    formatters = {
        'simple': {
            'format': '%(levelname)s - %(message)s'
        },
        'detailed': {
            '()': CustomFormatter,
            'format': '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'json': {
            '()': JSONFormatter
        }
    }
    
    # Define handlers
    handlers = {
        'console': {
            'class': 'logging.StreamHandler',
            'level': log_level,
            'formatter': 'detailed' if log_format != 'json' else 'json',
            'stream': sys.stdout
        }
    }
    
    # Add file handler if log_file is specified
    if log_file:
        handlers['file'] = {
            'class': 'logging.FileHandler',
            'level': log_level,
            'formatter': 'json' if enable_json_logs else 'detailed',
            'filename': log_file,
            'mode': 'a'
        }
    
    # Define loggers
    loggers = {
        'fastapi_app': {
            'level': log_level,
            'handlers': ['console'] + (['file'] if log_file else []),
            'propagate': False
        },
        'uvicorn.access': {
            'level': 'INFO',
            'handlers': ['console'] + (['file'] if log_file else []),
            'propagate': False
        },
        'uvicorn.error': {
            'level': 'INFO',
            'handlers': ['console'] + (['file'] if log_file else []),
            'propagate': False
        }
    }
    
    # Complete logging configuration
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': formatters,
        'handlers': handlers,
        'loggers': loggers,
        'root': {
            'level': log_level,
            'handlers': ['console'] + (['file'] if log_file else [])
        }
    }
    
    # Apply configuration
    logging.config.dictConfig(config)
    
    # Set color flag for console handler
    console_handler = logging.getLogger().handlers[0]
    if hasattr(console_handler, 'stream') and hasattr(console_handler.stream, 'isatty'):
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.addFilter(lambda record: setattr(record, 'color', True) or True)


def get_logger(name: str = "fastapi_app") -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)
