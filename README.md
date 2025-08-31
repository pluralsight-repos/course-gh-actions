# Simple FastAPI Project

A well-organized FastAPI application demonstrating GitHub Actions CI/CD workflows with proper project structure.

## 📁 Project Structure

```
.
├── app/                     # Main application package
│   ├── __init__.py
│   ├── main.py             # FastAPI app initialization
│   ├── core/               # Core functionality
│   │   ├── __init__.py
│   │   └── config.py       # Application settings
│   ├── models/             # Pydantic models
│   │   ├── __init__.py
│   │   └── item.py         # Item data models
│   └── routers/            # API route handlers
│       ├── __init__.py
│       └── items.py        # Items CRUD endpoints
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_main.py        # Main app tests
│   └── test_items.py       # Items API tests
├── docs/                   # Documentation
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── .gitignore             # Git ignore rules
└── .github/
    └── workflows/
        ├── test.yml        # Comprehensive CI/CD workflow
        └── api-build.yml   # Simple build workflow
```

## 🚀 Features

- **Modular Architecture**: Organized into logical packages
- **API Versioning**: Routes prefixed with `/api/v1`
- **Configuration Management**: Settings via environment variables
- **Comprehensive Testing**: Separate test modules for different components
- **Type Safety**: Full type hints with Pydantic models
- **Documentation**: Auto-generated API docs with FastAPI
- **Professional Logging**: Structured logging with request tracing
- **Request Middleware**: Automatic request/response logging with unique IDs
- **Multiple Log Formats**: Console, file, and JSON logging options

## 📡 API Endpoints

### Core Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check

### Items API (`/api/v1/items`)
- `GET /api/v1/items` - Get all items
- `GET /api/v1/items/{item_id}` - Get specific item
- `POST /api/v1/items` - Create new item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item

## Installation

### Option 1: Using Virtual Environment (Recommended)

1. **Create a virtual environment:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

2. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

### Option 2: Global Installation
```powershell
pip install -r requirements.txt
```

### Finding Your Virtual Environment

**Check if you're in a virtual environment:**
```powershell
python -c "import sys; print('Virtual env active:', hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))"
```

**Find your Python executable location:**
```powershell
python -c "import sys; print('Python path:', sys.executable)"
```

**Common virtual environment locations:**
- Current project: `.\venv\`
- User directory: `%USERPROFILE%\Envs\`
- Conda environments: `%USERPROFILE%\miniconda3\envs\` or `%USERPROFILE%\anaconda3\envs\`

## Running the Application

### Development Server

```powershell
# Run the application
python run.py
```

Or using uvicorn directly:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Running Tests

```powershell
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_items.py -v

# Run with coverage
pytest tests/ --cov=app
```

## 📊 Logging

This application includes comprehensive logging with the following features:

### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General application flow
- **WARNING**: Warning messages
- **ERROR**: Error conditions  
- **CRITICAL**: Critical error conditions

### Log Formats
- **Simple**: Basic level and message
- **Detailed**: Timestamp, level, module, line number, and message with colors
- **JSON**: Structured JSON format for log aggregation systems

### Request Tracing
Every HTTP request gets a unique `request_id` that's:
- Logged with all related log entries
- Added to response headers as `X-Request-ID`
- Used for tracking requests across the application

### Configuration
Configure logging via environment variables:

```bash
# .env file
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=detailed               # simple, detailed, json  
LOG_FILE=logs/app.log             # Path to log file
ENABLE_JSON_LOGS=false            # Enable JSON format for file logs
ENABLE_FILE_LOGGING=true          # Enable file logging
```

### Example Log Output

**Console (Detailed Format):**
```
2025-08-30 10:30:45 | INFO     | fastapi_app.middleware:45 | Incoming POST request to /api/v1/items
2025-08-30 10:30:45 | INFO     | fastapi_app.routers.items:35 | Creating new item: Test Item
2025-08-30 10:30:45 | INFO     | fastapi_app.middleware:67 | Request completed: POST /api/v1/items - 200
```

**JSON Format:**
```json
{
  "timestamp": "2025-08-30T10:30:45.123456",
  "level": "INFO",
  "logger": "fastapi_app.routers.items", 
  "message": "Creating new item: Test Item",
  "request_id": "abc123-def456-ghi789",
  "item_name": "Test Item",
  "item_price": 29.99
}
```

## Example Usage

### Create an item
```powershell
curl -X POST "http://localhost:8000/api/v1/items" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Example Item",
       "description": "This is an example item",
       "price": 29.99,
       "is_available": true
     }'
```

### Get all items
```powershell
curl http://localhost:8000/api/v1/items
```

### Get specific item
```powershell
curl http://localhost:8000/api/v1/items/1
```

### Update an item
```powershell
curl -X PUT "http://localhost:8000/api/v1/items/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Updated Item",
       "description": "Updated description",
       "price": 39.99,
       "is_available": true
     }'
```

### Delete an item
```powershell
curl -X DELETE "http://localhost:8000/api/v1/items/1"
```

## Project Structure

```
.
├── main.py              # FastAPI application
├── test_main.py         # Test suite
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .github/
    └── workflows/
        └── test.yml    # GitHub Actions workflow
```

## GitHub Actions

This project includes a GitHub Actions workflow that can be extended to:
- Run tests automatically
- Deploy the application
- Perform code quality checks
- Build and push Docker images
