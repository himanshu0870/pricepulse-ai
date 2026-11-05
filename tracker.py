import argparse
import sys
from app.database import SessionLocal, Base, engine
from app.models.product import Product
from app.services.price_engine import PriceEngine
from app.services.notification_service import NotificationService

Base.metadata.create_all(bind=engine)

def main():
    parser = argparse.ArgumentParser(description="PricePulse AI CLI")
    parser.add_argument("--list", action="store_true", help="List products")
    parser.add_argument("--run", action="store_true", help="Run scraping now")
    parser.add_argument("--test-notification", action="store_true", help="Test alerts")
    args = parser.parse_args()
    db = SessionLocal()

    if args.list:
        for p in db.query(Product).all():
            print(f"[{p.id}] {p.product_name} - {p.website_name}")
        sys.exit(0)

    if args.run:
        eng = PriceEngine(db)
        for p in db.query(Product).filter(Product.is_active == True).all():
            success, res = eng.execute_scrape(p)
            print(f"Scraped {p.product_name}: {'SUCCESS' if success else 'FAILED'}")
        sys.exit(0)

    if args.test_notification:
        notif = NotificationService(db)
        prod = Product(product_name="Test Item", product_url="https://example.com", website_name="Example")
        print("Telegram:", notif.send_telegram_alert(prod, 100, 80, "In Stock"))
        print("Discord:", notif.send_discord_alert(prod, 100, 80, "In Stock"))
        sys.exit(0)

    parser.print_help()

if __name__ == "__main__":
    main()
