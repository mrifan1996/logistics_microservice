from sqlalchemy import CheckConstraint, Column, Integer, Numeric, String

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("stock_quantity >= 0", name="non_negative_stock_check"),
        CheckConstraint("price >= 0", name="non_negative_price_check"),
    )
