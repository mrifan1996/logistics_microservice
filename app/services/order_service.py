from sqlalchemy.orm import Session

from app.enums import OrderStatus
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product


def create_order(db: Session, items: list):
    """
    items: list of OrderItemCreate (product_id, quantity)
    """
    if not items:
        raise ValueError("No items provided for order")

    # Start a transaction
    with db.begin_nested():  # ensures commit/rollback automatically
        # Lock products for update
        product_ids = [item.product_id for item in items]
        products = (
            db.query(Product)
            .filter(Product.id.in_(product_ids))
            .with_for_update()
            .all()
        )

        if len(products) != len(product_ids):
            raise ValueError("One or more products not found")

        product_map = {p.id: p for p in products}

        # Validate stock
        for item in items:
            product = product_map[item.product_id]
            if product.stock_quantity < item.quantity:
                raise ValueError(f"Insufficient stock for product {product.name}")

        # Deduct stock
        for item in items:
            product = product_map[item.product_id]
            product.stock_quantity -= item.quantity
            db.add(product)

        # Create order
        order = Order(status=OrderStatus.PENDING)
        db.add(order)
        db.flush()  # assigns order.id

        # Create order items
        order_items = []
        for item in items:
            product = product_map[item.product_id]
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity_ordered=item.quantity,
                price_at_time_of_order=product.price,
            )
            db.add(order_item)
            order_items.append(order_item)

        # Optional: attach items for response
        order.items = order_items

    return order
