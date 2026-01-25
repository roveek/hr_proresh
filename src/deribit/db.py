import datetime
import typing

import loguru
import pydantic
import pydantic_settings
import sqlalchemy.ext.asyncio
import sqlalchemy.orm

import deribit


class Config(pydantic_settings.BaseSettings):
    """Env переменные для БД"""

    database_url: pydantic.PostgresDsn


class DbAsyncRepository:
    """Репозиторий для асинхронной работы с БД Posgres"""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self._engine = sqlalchemy.ext.asyncio.create_async_engine(
            str(self.config.database_url),
        )

    def __repr__(self):
        return '<%s: %r>' % (
            self.__class__.__name__,
            self._engine,
        )

    @property
    def _session(self) -> sqlalchemy.ext.asyncio.AsyncSession:
        """Сессия для работы с БД

        Используется как асинхронный контекст-менеджер.
        """
        return sqlalchemy.ext.asyncio.async_sessionmaker(self._engine)

    async def create_price(self, ticker: str, price: float, timestamp: int):
        """Добавляет в БД прайс"""
        async with self._session() as session:
            async with session.begin():
                session.add(
                    deribit.models.Price(ticker=ticker, price=price,
                                         timestamp=timestamp),
                )

    async def iter_prices(self, ticker: str, yield_per: int = 100,
                          date: datetime.date | None = None
                          ) -> typing.AsyncGenerator[dict]:
        """Возвращает прайсы по одному (асинхронный генератор)

        :param ticker: фильтрация по тикеру валюты
        :param yield_per: запрашивает из БД по указанному кол-ву строк
        :param date: фильтрация по дате
        """
        seconds_in_day = 60 * 60 * 24
        async with self._session() as session:
            session: sqlalchemy.ext.asyncio.AsyncSession

            select = (
                sqlalchemy
                .select(deribit.models.Price)
                .where(deribit.models.Price.ticker == ticker)
            )

            if date is not None:
                start_ts = int(datetime.datetime.combine(date, datetime.time(0, 0)).timestamp())
                select = (
                    select
                    .where(deribit.models.Price.timestamp >= start_ts)
                    .where(deribit.models.Price.timestamp < start_ts + seconds_in_day)
                )
            select = select.order_by(deribit.models.Price.timestamp.desc())

            db_response: sqlalchemy.Result = await session.execute(select)

            for price_row in db_response.yield_per(yield_per):
                price_row: sqlalchemy.Row
                price = price_row._asdict()['Price']
                yield price.to_dict()


class DbService:

    repository_cls = DbAsyncRepository

    def __init__(self):
        try:
            self.repository = self.repository_cls()
        except Exception as exc:
            loguru.logger.error('Failed to initialize DB repository',
                                exc_info=exc)
            raise

    def __repr__(self):
        return '<%s: %r>' % (
            self.__class__.__name__,
            self.repository,
        )

    async def create_price(self, price: deribit.schema.Price):
        """Добавляет в БД прайс"""
        kwargs = price.model_dump(include={'ticker', 'price', 'timestamp'})
        await self.repository.create_price(**kwargs)

    async def get_last_price(self, ticker: str) -> deribit.schema.Price | None:
        """Возвращает последний прайс указанного тикера"""
        with loguru.logger.catch():
            price = await anext(self.repository.iter_prices(ticker, yield_per=1), None)
            if price:
                price = deribit.schema.Price(**price)
            return price

    async def get_all_prices(self, ticker: str,
                             date: datetime.date | None = None,
                             ) -> list[deribit.schema.Price]:
        """Возвращает все прайсы указанного тикера с фильтрацией по дате"""
        prices = []
        async for price in self.repository.iter_prices(ticker, date=date):
            prices.append(deribit.schema.Price(**price))
        return prices
