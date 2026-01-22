import aiohttp
import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    ...


class DbRepository:

    def __init__(self):
        self._db = aiohttp.ClientSession()


class DbService:
    ...
