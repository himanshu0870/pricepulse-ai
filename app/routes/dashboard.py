from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.models.scraping_log import ScrapingLog

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    return {
        "total_products": db.query(Product).count(),
        "active_monitoring": db.query(Product).filter(Product.is_active == True).count(),
        "successful_scrapes": db.query(ScrapingLog).filter(ScrapingLog.status == "SUCCESS").count(),
        "failed_scrapes": db.query(ScrapingLog).filter(ScrapingLog.status == "FAILED").count(),
        "out_of_stock_count": 0
    }
