from sqlalchemy import Column, Integer, String, Numeric, CheckConstraint
from .base import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("stock_quantity >= 0", name="ck_stock_non_negative"),
        CheckConstraint("price >= 0", name="ck_price_non_negative"),
    )