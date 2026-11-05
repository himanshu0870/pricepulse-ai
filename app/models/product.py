from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    group_id = Column(String(100), nullable=True, index=True)
    product_name = Column(String(255), nullable=False)
    product_url = Column(String(2048), nullable=False)
    website_name = Column(String(100), nullable=False)
    target_price = Column(Float, nullable=True)
    monitoring_interval = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="products")
    price_histories = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="product", cascade="all, delete-orphan")
    scraping_logs = relationship("ScrapingLog", back_populates="product", cascade="all, delete-orphan")
