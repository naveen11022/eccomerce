from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    items = relationship("CartItem", back_populates="cart", cascade="all, delete")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)

    cart = relationship("Cart", back_populates="items")
