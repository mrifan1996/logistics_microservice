from typing import List
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: Decimal = Field(..., ge=0)
    stock_quantity: int = Field(..., ge=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True)

class PaginatedProducts(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    items: List[ProductResponse]