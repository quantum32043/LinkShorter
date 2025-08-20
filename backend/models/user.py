from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base
from backend.models.history import History


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()

    history: Mapped[List["History"]] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password_hash={self.password_hash!r})"
