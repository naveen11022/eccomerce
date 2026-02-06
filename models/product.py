from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
