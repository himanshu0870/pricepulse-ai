from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    notification_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    channel = Column(String(20), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    delivery_status = Column(String(20), default="SENT")
    product = relationship("Product", back_populates="notifications")
