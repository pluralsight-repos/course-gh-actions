import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_items_empty():
    """Test getting items when database is empty"""
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert response.json() == []
    # Check that request ID header is present
    assert "X-Request-ID" in response.headers

def test_create_item():
    """Test creating a new item"""
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 29.99,
        "is_available": True
    }
    response = client.post("/api/v1/items", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["price"] == item_data["price"]
    assert "id" in data
    assert "X-Request-ID" in response.headers

def test_get_item():
    """Test getting a specific item"""
    # First create an item
    item_data = {
        "name": "Test Item 2",
        "description": "Another test item",
        "price": 19.99,
        "is_available": True
    }
    create_response = client.post("/api/v1/items", json=item_data)
    created_item = create_response.json()
    
    # Then get the item
    response = client.get(f"/api/v1/items/{created_item['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]

def test_get_nonexistent_item():
    """Test getting an item that doesn't exist"""
    response = client.get("/api/v1/items/999")
    assert response.status_code == 404

def test_update_item():
    """Test updating an item"""
    # First create an item
    item_data = {
        "name": "Original Item",
        "description": "Original description",
        "price": 10.00,
        "is_available": True
    }
    create_response = client.post("/api/v1/items", json=item_data)
    created_item = create_response.json()
    
    # Update the item
    updated_data = {
        "name": "Updated Item",
        "description": "Updated description",
        "price": 15.00,
        "is_available": False
    }
    response = client.put(f"/api/v1/items/{created_item['id']}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["price"] == updated_data["price"]

def test_delete_item():
    """Test deleting an item"""
    # First create an item
    item_data = {
        "name": "Item to Delete",
        "description": "This will be deleted",
        "price": 5.00,
        "is_available": True
    }
    create_response = client.post("/api/v1/items", json=item_data)
    created_item = create_response.json()
    
    # Delete the item
    response = client.delete(f"/api/v1/items/{created_item['id']}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/items/{created_item['id']}")
    assert get_response.status_code == 404
