from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.enums import OrderStatus
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import create_order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_endpoint(payload: OrderCreate, db: Session = Depends(get_db)):
    try:
        order = create_order(db, payload.items)
        return order
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int, status: OrderStatus, db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(400, "Cannot modify a cancelled order")

    if order.status == OrderStatus.SHIPPED:
        raise HTTPException(400, "Order already shipped")

    order.status = status
    db.commit()
    return {"status": order.status}
