import aiohttp


class BaseHttpRepository:

    async def get(self, url: str) -> dict:
        """GET-запрос"""
        async with aiohttp.client.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
