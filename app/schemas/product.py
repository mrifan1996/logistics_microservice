from pydantic import BaseModel, Field
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

    class Config:
        from_attributes = True
