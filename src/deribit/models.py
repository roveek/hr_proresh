import time

import sqlalchemy.orm
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

Base = sqlalchemy.orm.declarative_base()


class Price(Base):

    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    ticker: Mapped[str] = mapped_column(index=True)
    price: Mapped[float] = mapped_column()
    timestamp: Mapped[int] = mapped_column(default=lambda: int(time.time()))
