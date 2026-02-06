from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Numeric(10, 2))
    status = Column(String(50), default="PLACED")

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Numeric(10, 2))

    order = relationship("Order", back_populates="items")
