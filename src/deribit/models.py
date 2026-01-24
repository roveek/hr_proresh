import time

import sqlalchemy.orm
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(sqlalchemy.orm.DeclarativeBase):

    def to_dict(self) -> dict:
        return self.__dict__


class Price(Base):

    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    ticker: Mapped[str] = mapped_column(index=True)
    price: Mapped[float] = mapped_column()
    timestamp: Mapped[int] = mapped_column(default=lambda: int(time.time()))
