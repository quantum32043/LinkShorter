from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import TYPE_CHECKING

from backend.models.base import Base

if TYPE_CHECKING:
    from backend.models.user import User


class History(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    original_link: Mapped[str] = mapped_column()
    short_link: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()

    user: Mapped[User] = relationship(back_populates="history")

    def __repr__(self) -> str:
        return (f"History(id={self.id!r}, user_id={self.user_id!r}, original_link={self.original_link!r}, "
                f"short_link={self.short_link!r} date={self.date!r})")
