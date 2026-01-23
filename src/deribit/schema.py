import time

import pydantic


class Price(pydantic.BaseModel):

    ticker: str
    price: float
    timestamp: int = pydantic.Field(default_factory=lambda: int(time.time()))
