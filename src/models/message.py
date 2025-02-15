
from datetime import datetime
from sqlalchemy import  DateTime, ForeignKey 
from src.config.database import Base
from sqlalchemy.orm import Mapped,mapped_column , relationship 
from sqlalchemy.ext.asyncio import AsyncAttrs

class Message(Base,AsyncAttrs):

    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime)

    
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    sender: Mapped["User"] = relationship(foreign_keys=[sender_id])

    
    receiver_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    receiver: Mapped["User"] = relationship(foreign_keys=[receiver_id])