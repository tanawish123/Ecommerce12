from pydantic import BaseModel
from datetime import date
from typing import Optional
class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock: int

class Sale(BaseModel):
    id: int
    product_id: int
    quantity: int
    sale_date: date
class Category(BaseModel):
    id: int
    name: str

class Inventory(BaseModel):
    id: int
    product_id: int
    stock: int
    change_type: Optional[str]
    quantity: int
    change_date: date
    reference: Optional[str]
