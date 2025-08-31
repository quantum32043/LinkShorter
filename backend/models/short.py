from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base


class Short(Base):
    __tablename__ = 'short'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    original_link: Mapped[str] = mapped_column()
    short_link: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column()


    def __repr__(self) -> str:
        return (f"Short(id={self.id!r}, original_link={self.original_link!r}, "
                f"short_link={self.short_link!r} date={self.date!r})")
