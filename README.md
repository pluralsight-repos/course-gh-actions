# Simple FastAPI Project

A simple FastAPI application for demonstrating GitHub Actions CI/CD workflows.

## Features

- RESTful API with CRUD operations
- Item management (Create, Read, Update, Delete)
- Health check endpoint
- Automatic API documentation with Swagger UI
- Comprehensive test suite

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /items` - Get all items
- `GET /items/{item_id}` - Get specific item
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

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

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Running Tests

```bash
pytest test_main.py -v
```

## Example Usage

### Create an item
```bash
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Example Item",
       "description": "This is an example item",
       "price": 29.99,
       "is_available": true
     }'
```

### Get all items
```bash
curl http://localhost:8000/items
```

### Get specific item
```bash
curl http://localhost:8000/items/1
```

### Update an item
```bash
curl -X PUT "http://localhost:8000/items/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Updated Item",
       "description": "Updated description",
       "price": 39.99,
       "is_available": true
     }'
```

### Delete an item
```bash
curl -X DELETE "http://localhost:8000/items/1"
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
