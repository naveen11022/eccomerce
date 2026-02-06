from pydantic import BaseModel
from decimal import Decimal


class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int

    class Config:
        from_attributes = True
