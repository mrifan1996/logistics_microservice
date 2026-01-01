from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    CANCELLED = "Cancelled"
