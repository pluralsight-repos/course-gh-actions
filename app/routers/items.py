from fastapi import APIRouter, HTTPException
from typing import List
from ..models.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter()

# In-memory storage (for demo purposes)
items_db = []
next_id = 1


@router.get("/items", response_model=List[ItemResponse])
async def get_items():
    """Get all items"""
    return items_db


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    """Create a new item"""
    global next_id
    new_item = {
        "id": next_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "is_available": item.is_available
    }
    items_db.append(new_item)
    next_id += 1
    return new_item


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item"""
    existing_item = next((item for item in items_db if item["id"] == item_id), None)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    existing_item.update({
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "is_available": item.is_available
    })
    return existing_item


@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    global items_db
    original_length = len(items_db)
    items_db = [item for item in items_db if item["id"] != item_id]
    
    if len(items_db) == original_length:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": f"Item {item_id} deleted successfully"}
