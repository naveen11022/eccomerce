from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db_dependency
from models.product import Product
from schemas.cart import CartItemOut
from config.redis_config import config
from utils.token import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add")
def add_to_cart(
    data: CartItemOut,
    db: Session = Depends(get_db_dependency),
    user = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == data.product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    if product.stock < data.quantity:
        raise HTTPException(400, "Insufficient stock")

    cart_key = f"cart:{user.id}"

    config.hincrby(cart_key, data.product_id, data.quantity)

    return {"message": "Product added to cart"}


@router.get("/")
def get_cart(
    db: Session = Depends(get_db_dependency),
    user = Depends(get_current_user)
):
    cart_key = f"cart:{user.id}"
    cart_items = config.hgetall(cart_key)

    if not cart_items:
        return {"items": [], "total": 0}

    product_ids = [int(pid.decode()) for pid in cart_items.keys()]

    products = db.query(Product).filter(Product.id.in_(product_ids)).all()

    product_map = {p.id: p for p in products}

    response_items = []
    total = 0

    for pid_b, qty_b in cart_items.items():
        pid = int(pid_b.decode())
        qty = int(qty_b.decode())

        product = product_map.get(pid)
        if not product:
            continue

        item_total = product.price * qty
        total += item_total

        response_items.append({
            "product_id": pid,
            "name": product.name,
            "price": product.price,
            "quantity": qty,
            "total": item_total
        })

    return {
        "items": response_items,
        "total": total
    }


@router.delete("/remove/{product_id}")
def remove_from_cart(
    product_id: int,
    user = Depends(get_current_user)
):
    cart_key = f"cart:{user.id}"
    config.hdel(cart_key, product_id)

    return {"message": "Item removed"}


@router.delete("/clear")
def clear_cart(user = Depends(get_current_user)):
    config.delete(f"cart:{user.id}")
    return {"message": "Cart cleared"}
