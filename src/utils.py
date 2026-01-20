import aiohttp


class BaseFetch:

    # Асинхронный http-клиент на выбор
    _http_client = aiohttp.client.ClientSession
    # _http_client = httpx.AsyncClient

    async def get(self, url: str) -> dict:
        """GET-запрос"""
        async with self._http_client() as session:
            async with session.get(url) as response:
                return await response.json()
