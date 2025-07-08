from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.database import Base
from app.schemas import ComplaintReturn

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
            status=self.status,
            sentiment=self.sentiment,
            category=self.category
        )