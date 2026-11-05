from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ScrapingLog(Base):
    __tablename__ = "scraping_logs"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    status = Column(String(20), nullable=False)
    error_message = Column(Text, nullable=True)
    execution_time = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    product = relationship("Product", back_populates="scraping_logs")
