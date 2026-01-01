from typing import Generator
import pytest
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.product import Product
from app.services.order_service import create_order
from app.schemas.order import OrderItemCreate
from app.enums import OrderStatus

@pytest.fixture
def db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()   # rollback test data
        db.close()


def test_create_order_success_reduces_stock(db: Session):
    product = Product(
        name="Test Product",
        price=100,
        stock_quantity=10
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    order = create_order(
        db,
        items=[
            OrderItemCreate(product_id=product.id, quantity=3)
        ]
    )

    db.refresh(product)

    assert order.status == OrderStatus.PENDING
    assert product.stock_quantity == 7
    assert len(order.items) == 1


def test_create_order_insufficient_stock_raises_error(db: Session):
    product = Product(
        name="Low Stock Product",
        price=50,
        stock_quantity=2
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    with pytest.raises(ValueError, match="Insufficient stock"):
        create_order(
            db,
            items=[
                OrderItemCreate(product_id=product.id, quantity=5)
            ]
        )


def test_create_order_insufficient_stock_does_not_change_stock(db: Session):
    product = Product(
        name="Rollback Product",
        price=200,
        stock_quantity=4
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    try:
        create_order(
            db,
            items=[
                OrderItemCreate(product_id=product.id, quantity=10)
            ]
        )
    except ValueError:
        pass

    db.refresh(product)
    assert product.stock_quantity == 4
