import time

import sqlalchemy.orm


Base = sqlalchemy.orm.declarative_base()


class Price(Base):

    __tablename__ = 'prices'

    ticker = sqlalchemy.Column(sqlalchemy.String(10), primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.Float)
    timestamp = sqlalchemy.Column(sqlalchemy.BigInteger,
                                  default=lambda: int(time.time()))
