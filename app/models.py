from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.database import Base
from app.schemas import ComplaintReturn, ComplaintToN8n

class Complaint(Base):
    __tablename__ = "complaints"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="open")
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    sentiment: Mapped[str] = mapped_column(String, default="unknown")
    category: Mapped[str] = mapped_column(String, default="другое")

    def to_schema(self) -> ComplaintReturn:
        return ComplaintReturn(
            id=self.id,
            text=self.text,
            status=self.status,
            sentiment=self.sentiment,
            category=self.category
        )
    
    def to_n8n(self) -> ComplaintToN8n:
        return ComplaintToN8n(
            id=self.id,
            text=self.text,
            sentiment=self.sentiment,
            date=str(self.timestamp),
            category=self.category,
        )
    
    def __repr__(self):
        return str(self.id)+" "+str(self.text)