import requests
import logging
from sqlalchemy.orm import Session
from app.config import settings
from app.models.product import Product
from app.models.notification import Notification

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def send_telegram_alert(self, product: Product, prev_price: float, curr_price: float, stock_status: str) -> bool:
        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            return False
        message = f"🚨 *PRICE DROP!*\n📦 *Product:* {product.product_name}\n💰 *New Price:* ₹{curr_price:,.2f}"
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        res = requests.post(url, json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=10)
        return res.status_code == 200

    def send_discord_alert(self, product: Product, prev_price: float, curr_price: float, stock_status: str) -> bool:
        if not settings.DISCORD_WEBHOOK_URL:
            return False
        payload = {"embeds": [{"title": "🚨 Price Drop Alert", "description": f"**{product.product_name}** is now ₹{curr_price:,.2f}"}]}
        res = requests.post(settings.DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        return res.status_code in [200, 204]
