from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class InventoryChange(BaseModel):
    product_id: int = Field(..., description="Product ID")
    change_type: str = Field(..., description="Type of inventory change")
    quantity: int = Field(..., description="Quantity changed")
    reference: Optional[str] = Field(None, description="Optional reference (e.g. sale ID)")

    @field_validator('change_type')
    def validate_change_type(cls, v):
        allowed = {'IN', 'OUT', 'ADJUSTMENT'}
        if v not in allowed:
            raise ValueError(f'change_type must be one of {allowed}')
        return v

    @field_validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('quantity must be greater than 0')
        return v
class InventoryStatus(BaseModel):
    product_id: int
    stock: int = Field(..., description="Current stock level")
    last_updated: datetime = Field(..., description="Timestamp of last stock update")