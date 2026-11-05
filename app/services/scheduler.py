import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models.product import Product
from app.services.price_engine import PriceEngine

logger = logging.getLogger(__name__)

def run_scheduled_monitoring_job():
    db = SessionLocal()
    try:
        engine = PriceEngine(db)
        products = db.query(Product).filter(Product.is_active == True).all()
        for product in products:
            engine.execute_scrape(product)
    finally:
        db.close()

class PricePulseScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self, interval_minutes: int = 30):
        self.scheduler.add_job(run_scheduled_monitoring_job, 'interval', minutes=interval_minutes, id='tracker_job', replace_existing=True)
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()
