import uuid
from datetime import datetime

from sqlalchemy import TEXT, TIMESTAMP, Integer, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class Short(Base):
    __tablename__ = 'short'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    original_link: Mapped[str] = mapped_column(TEXT)
    short_link: Mapped[str] = mapped_column(TEXT)
    date: Mapped[datetime] = mapped_column(TIMESTAMP)

    user: Mapped["User"] = relationship("User", back_populates="short_links")

    def __repr__(self) -> str:
        return (f"Short(id={self.id!r}, session_id={self.session_id!r}, user_id={self.user_id!r}, original_link={self.original_link!r}, "
                f"short_link={self.short_link!r} date={self.date!r})")
