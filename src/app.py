import datetime
from typing import Annotated

import fastapi
from fastapi import Query

import deribit.db

app = fastapi.FastAPI()

TickerAnnotation = Annotated[
    str,
    Query(description='Тикер валюты',
          # `example` has been deprecated,
          # но в таком виде пример подставляется в поле ввода в /docs
          example='btc_usd')
]
DateFilterAnnotation = Annotated[
    datetime.date | None,
    Query(description='Только прайсы за указанную дату',
          example=datetime.datetime.now().date().isoformat())
]


@app.get("/healthcheck",
         include_in_schema=False)
async def health_check():
    """Технический endpoint"""

    return {"status": "healthy"}


@app.get("/prices/last")
async def get_last_price(ticker: TickerAnnotation
                         ) -> deribit.schema.Price:
    """Возвращает последний прайс по указанному тикеру"""

    price = await deribit.db.service.get_last_price(ticker)
    if price is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND)
    return price


@app.get("/prices")
async def get_last_price(ticker: TickerAnnotation,
                         date: DateFilterAnnotation = None
                         ) -> list[deribit.schema.Price]:
    """Возвращает все прайсы по указанному тикеру"""

    prices = await deribit.db.service.get_all_prices(ticker, date)
    return prices
