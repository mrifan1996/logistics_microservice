from enum import Enum


# Using str here makes it more compatible with pydantic due to easy serialization
class OrderStatus(str, Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"
