from fastapi import APIRouter, HTTPException, Request
from typing import List
from ..models.item import ItemCreate, ItemUpdate, ItemResponse
from ..core.logging import get_logger

router = APIRouter()
logger = get_logger("fastapi_app.routers.items")

# In-memory storage (for demo purposes)
items_db = []
next_id = 1


@router.get("/items", response_model=List[ItemResponse])
async def get_items(request: Request):
    """Get all items"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    logger.info(f"Fetching all items - found {len(items_db)} items", 
                extra={"request_id": request_id, "items_count": len(items_db)})
    return items_db


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, request: Request):
    """Get a specific item by ID"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    logger.info(f"Fetching item with ID: {item_id}", 
                extra={"request_id": request_id, "item_id": item_id})
    
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        logger.warning(f"Item not found: {item_id}", 
                      extra={"request_id": request_id, "item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    
    logger.debug(f"Item found: {item['name']}", 
                extra={"request_id": request_id, "item_id": item_id, "item_name": item['name']})
    return item


@router.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate, request: Request):
    """Create a new item"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    global next_id
    
    logger.info(f"Creating new item: {item.name}", 
                extra={"request_id": request_id, "item_name": item.name, "item_price": item.price})
    
    new_item = {
        "id": next_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "is_available": item.is_available
    }
    items_db.append(new_item)
    
    logger.info(f"Item created successfully with ID: {next_id}", 
                extra={"request_id": request_id, "item_id": next_id, "item_name": item.name})
    
    next_id += 1
    return new_item


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate, request: Request):
    """Update an existing item"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    logger.info(f"Updating item with ID: {item_id}", 
                extra={"request_id": request_id, "item_id": item_id})
    
    existing_item = next((item for item in items_db if item["id"] == item_id), None)
    if not existing_item:
        logger.warning(f"Cannot update - item not found: {item_id}", 
                      extra={"request_id": request_id, "item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Log changes
    old_name = existing_item.get("name")
    old_price = existing_item.get("price")
    
    existing_item.update({
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "is_available": item.is_available
    })
    
    logger.info(f"Item updated successfully: {item_id}", 
                extra={
                    "request_id": request_id, 
                    "item_id": item_id, 
                    "old_name": old_name,
                    "new_name": item.name,
                    "old_price": old_price,
                    "new_price": item.price
                })
    
    return existing_item


@router.delete("/items/{item_id}")
async def delete_item(item_id: int, request: Request):
    """Delete an item"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    logger.info(f"Deleting item with ID: {item_id}", 
                extra={"request_id": request_id, "item_id": item_id})
    
    global items_db
    original_length = len(items_db)
    item_to_delete = next((item for item in items_db if item["id"] == item_id), None)
    
    if not item_to_delete:
        logger.warning(f"Cannot delete - item not found: {item_id}", 
                      extra={"request_id": request_id, "item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db = [item for item in items_db if item["id"] != item_id]
    
    logger.info(f"Item deleted successfully: {item_id} - '{item_to_delete['name']}'", 
                extra={
                    "request_id": request_id, 
                    "item_id": item_id, 
                    "deleted_item_name": item_to_delete['name']
                })
    
    return {"message": f"Item {item_id} deleted successfully"}
