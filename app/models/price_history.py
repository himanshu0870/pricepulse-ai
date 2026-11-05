from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    current_price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    stock_status = Column(String(50), default="Unknown")
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    product = relationship("Product", back_populates="price_histories")
