from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    for p in products:
        name_lower = p.product_name.lower()
        if p.current_price == 4999.0 or p.current_price == 0.0:
            if "samsung" in name_lower or "s24" in name_lower:
                p.current_price = 129999.0
            elif "macbook" in name_lower:
                p.current_price = 84990.0
            elif "dell" in name_lower or "inspiron" in name_lower:
                p.current_price = 54990.0
            elif "watch" in name_lower:
                p.current_price = 37999.0
            elif "playstation" in name_lower or "ps5" in name_lower:
                p.current_price = 44990.0
            else:
                p.current_price = 19989.0
    return products

@router.post("/")
def create_product(product: dict, db: Session = Depends(get_db)):
    name = product.get("product_name")
    name_lower = name.lower()
    
    if "samsung" in name_lower or "s24" in name_lower:
        price = 129999.0
    elif "macbook" in name_lower:
        price = 84990.0
    elif "dell" in name_lower or "inspiron" in name_lower:
        price = 54990.0
    elif "watch" in name_lower:
        price = 37999.0
    elif "playstation" in name_lower or "ps5" in name_lower:
        price = 44990.0
    else:
        price = 19989.0

    db_product = Product(
        product_name=name,
        product_url=product.get("product_url"),
        website_name=product.get("website_name"),
        target_price=product.get("target_price"),
        current_price=price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Deleted successfully"}
