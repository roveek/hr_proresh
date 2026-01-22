import pathlib

import pydantic
import pydantic_settings

import utils


class Config(pydantic_settings.BaseSettings):

    deribit_url: pydantic.HttpUrl = 'https://test.deribit.com/api/v2'

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=pathlib.Path(__file__).parent / '.env',
    )


class FetchHttpRepository(utils.BaseFetchHttp):
    """Репозиторий отвечает за получение данных от API Deribit"""

    def __init__(self, config=None):
        self.config = config or Config()

    async def fetch_index_price(self, index_name: str) -> dict:
        url_path = f'public/get_index_price?index_name={index_name}'
        url = f'{self.config.deribit_url}/{url_path}'
        return await self.get(url)


class FetchSerice:
    """Сервис отвечает за извлечение данных из ответа API Deribit"""

    def __init__(self):
        self.repository = FetchHttpRepository()

    async def btc_usd(self) -> float:
        return await self._fetch_index_price('btc_usd')

    async def eth_usd(self) -> float:
        return await self._fetch_index_price('eth_usd')

    async def _fetch_index_price(self, index_name: str) -> float:
        return self._extract_index_price(
            await self.repository.fetch_index_price(index_name)
        )

    def _extract_index_price(self, price_jsonrpc2: dict) -> float:
        return price_jsonrpc2.get('result', {}).get('index_price')
