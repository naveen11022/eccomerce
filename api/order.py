from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from database.database import get_db_dependency
from config.redis_config import config
from models.product import Product
from models.order import Order
from models.order import OrderItem
from utils.token import get_current_user
from config.celery_app import send_order_email
import json

router = APIRouter(prefix="/order", tags=["Order"])


@router.post("/place", status_code=status.HTTP_201_CREATED)
def place_order(
    db: Session = Depends(get_db_dependency),
    user = Depends(get_current_user),
    idempotency_key: str = Header(...)
):
    redis_key = f"order:idempotency:{user.id}:{idempotency_key}"

    cached_response = config.get(redis_key)
    if cached_response:
        return json.loads(cached_response)

    cart_key = f"cart:{user.id}"
    cart = config.hgetall(cart_key)

    if not cart:
        raise HTTPException(400, "Cart is empty")

    product_ids = [int(pid.decode()) for pid in cart.keys()]
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    product_map = {p.id: p for p in products}

    total_amount = 0
    order_items = []

    for pid_b, qty_b in cart.items():
        pid = int(pid_b.decode())
        qty = int(qty_b.decode())

        product = product_map.get(pid)
        if not product:
            raise HTTPException(404, f"Product {pid} not found")

        if product.stock < qty:
            raise HTTPException(
                400,
                f"Insufficient stock for {product.name}"
            )

        total_amount += product.price * qty
        order_items.append((product, qty))

    order = Order(
        user_id=user.id,
        total_amount=total_amount
    )
    db.add(order)
    db.flush()

    for product, qty in order_items:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=qty,
                price=product.price
            )
        )
        product.stock -= qty

    db.commit()

    config.delete(cart_key)

    response = {
        "order_id": order.id,
        "total": total_amount,
        "message": "Order placed successfully"
    }
    send_order_email.delay(
        user.email,
        order.id
    )

    config.setex(
        redis_key,
        600,
        json.dumps(response)
    )

    return response
