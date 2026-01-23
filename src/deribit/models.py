import time

import sqlalchemy.orm


Base = sqlalchemy.orm.declarative_base()


class Price(Base):

    __tablename__ = 'prices'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    ticker = sqlalchemy.Column(sqlalchemy.String(10))
    price = sqlalchemy.Column(sqlalchemy.Float)
    timestamp = sqlalchemy.Column(sqlalchemy.BigInteger,
                                  default=lambda: int(time.time()))
