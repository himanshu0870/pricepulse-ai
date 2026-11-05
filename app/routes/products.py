from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.product import Product
from app.models.price_history import PriceHistory

router = APIRouter(prefix="/api/products", tags=["Products"])

class ProductCreate(BaseModel):
    product_name: str
    product_url: str
    website_name: str
    target_price: Optional[float] = None

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    results = []
    for p in products:
        latest = db.query(PriceHistory).filter(PriceHistory.product_id == p.id).order_by(PriceHistory.recorded_at.desc()).first()
        results.append({
            "id": p.id,
            "product_name": p.product_name,
            "product_url": p.product_url,
            "website_name": p.website_name,
            "target_price": p.target_price,
            "is_active": p.is_active,
            "current_price": latest.current_price if latest else 0.0,
            "stock_status": latest.stock_status if latest else "Unknown"
        })
    return results

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(prod: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**prod.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(prod)
    db.commit()
    return {"message": "Product deleted successfully"}
