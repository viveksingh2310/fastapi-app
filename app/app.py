from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI(
    title="FastAPI CI/CD Demo App",
    description="Sample FastAPI app for Jenkins + Docker pipeline",
    version="1.0.0"
)

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class Item(BaseModel):
    id: int
    name: str
    price: float

ITEMS_DB: List[Item] = [
    Item(id=1, name="Laptop", price=75000.0),
    Item(id=2, name="Mouse", price=1200.0)
]
@app.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "UP",
        "timestamp": datetime.utcnow()
    }

@app.get("/")
def root():
    return {
        "message": "FastAPI application running successfully 🚀"
    }

@app.get("/items", response_model=List[Item])
def get_items():
    return ITEMS_DB
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in ITEMS_DB:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    for existing_item in ITEMS_DB:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Item ID already exists")

    ITEMS_DB.append(item)
    return item
