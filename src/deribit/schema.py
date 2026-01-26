import time

import pydantic


class Price(pydantic.BaseModel):

    ticker: str = pydantic.Field(description='Тикер валюты')
    price: float = pydantic.Field(description='Цена')
    timestamp: int = pydantic.Field(
        description='Дата и время в unix timestamp (UTC)',
        default_factory=lambda: int(time.time()))

    model_config = pydantic.ConfigDict(
        extra='ignore',
    )
