from pydantic import BaseModel
from decimal import Decimal


class CartItemOut(BaseModel):
    product_id: int
    quantity: int


class CartOut(BaseModel):
    items: list[CartItemOut]
