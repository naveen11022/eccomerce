from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db_dependency
from models.product import Product
from schemas.product import ProductOut

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db_dependency)):
    return db.query(Product).filter(Product.is_active == True).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db_dependency)):
    return db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()
