from typing import List

from sqlalchemy import Integer, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(TEXT, unique=True)
    password_hash: Mapped[str] = mapped_column(VARCHAR)
    refresh_token: Mapped[str] = mapped_column(VARCHAR, nullable=True)

    short_links: Mapped[List["Short"]] = relationship("Short", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password_hash={self.password_hash!r})"
