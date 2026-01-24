import datetime
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

    @pydantic.computed_field(
        description='Дата и время в человеческом формате (для наглядности)',
        # …и демонстрации работы с computed_field
    )
    @property
    def timestamp_as_dt(self) -> str:
        return datetime.datetime.fromtimestamp(self.timestamp).isoformat(sep=' ')
