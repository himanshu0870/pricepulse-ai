import time
import logging
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.scraping_log import ScrapingLog
from app.scrapers.generic_scraper import GenericScraper
from app.scrapers.playwright_scraper import PlaywrightScraper

logger = logging.getLogger(__name__)

class PriceEngine:
    def __init__(self, db: Session):
        self.db = db
        self.generic_scraper = GenericScraper()
        self.playwright_scraper = PlaywrightScraper()

    def execute_scrape(self, product: Product, use_playwright: bool = False, custom_selectors: Dict[str, str] = None) -> Tuple[bool, Dict[str, Any]]:
        start_time = time.time()
        try:
            scraper = self.playwright_scraper if use_playwright else self.generic_scraper
            data = scraper.scrape(product.product_url, custom_selectors=custom_selectors)
            exec_time = time.time() - start_time
            
            log = ScrapingLog(product_id=product.id, status="SUCCESS", execution_time=round(exec_time, 3))
            self.db.add(log)
            
            history = PriceHistory(
                product_id=product.id,
                current_price=data["current_price"],
                original_price=data.get("original_price"),
                stock_status=data.get("stock_status", "In Stock")
            )
            self.db.add(history)
            self.db.commit()
            return True, data
        except Exception as e:
            exec_time = time.time() - start_time
            log = ScrapingLog(product_id=product.id, status="FAILED", error_message=str(e), execution_time=round(exec_time, 3))
            self.db.add(log)
            self.db.commit()
            return False, {"error": str(e)}
