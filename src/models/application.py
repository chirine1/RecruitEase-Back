
from datetime import datetime
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from src.config.database import Base
from src.models.enums import Decision
from sqlalchemy.orm import Mapped,mapped_column , relationship


class Application(Base, AsyncAttrs):

    __tablename__ = "application"

    id: Mapped[int] = mapped_column(primary_key=True)
    motivation_letter: Mapped[str] = mapped_column(String(200))
    decision: Mapped[Decision] = mapped_column(Enum(Decision), default=Decision.pending)
    created_at: Mapped[datetime|None] = mapped_column(default=datetime.now())

    candidate: Mapped["Candidate"] = relationship(lazy="selectin")
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.id"))

    job: Mapped["Job"] = relationship(lazy="selectin")
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
