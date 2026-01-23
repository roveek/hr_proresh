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

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self._engine = sqlalchemy.ext.asyncio.create_async_engine(
            str(self.config.database_url),
        )

    @property
    def _session(self) -> sqlalchemy.ext.asyncio.AsyncSession:
        return sqlalchemy.ext.asyncio.async_sessionmaker(self._engine)

    async def create_price(self, ticker: str, price: float, timestamp: int):
        async with self._session() as session:
            async with session.begin():
                session.add(
                    deribit.models.Price(ticker=ticker, price=price,
                                         timestamp=timestamp),
                )

    async def get_price(self, ticker: str):
        async with self._session() as session:
            (session
             .query(deribit.models.Price)
             .filter(deribit.models.Price.ticker == ticker)
             .order_by(deribit.models.Price.timestamp.desc())
             )

    async def iter_price(self, ticker: str):
        async with self._session() as session:
            yield (
                session
                .query(deribit.models.Price)
                .filter(deribit.models.Price.ticker == ticker)
                .order_by(deribit.models.Price.timestamp.desc(),)
                .yield_per(1)
            )


class DbService:

    def __init__(self):
        try:
            self.repository = DbAsyncRepository()
        except Exception as exc:
            loguru.logger.error('Failed to initialize DB repository', exc_info=exc)
            raise

    async def create_price(self, price: deribit.schema.Price):
        await self.repository.create_price(**price.model_dump())

    async def get_last_price(self, ticker: str) -> deribit.schema.Price:
        ...


service = DbService()
