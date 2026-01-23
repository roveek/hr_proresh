import asyncio

import celery
import loguru

import deribit


@celery.shared_task
def fetch_prices():
    loguru.logger.info('Fetching prices task')
    asyncio.get_event_loop().run_until_complete(_process_fetch_prices())
    return 'OK'


@loguru.logger.catch()
async def _process_fetch_prices():
    prices = await _fetch_prices()
    loguru.logger.info(f'Fetched {prices=}')
    await _save_prices(prices)


async def _fetch_prices() -> list[deribit.schema.Price]:
    btc_usd = await deribit.api.service.fetch_btc_usd_price()
    eth_usd = await deribit.api.service.fetch_eth_usd_price()

    return [
        deribit.schema.Price(ticker='btc_usd', price=btc_usd),
        deribit.schema.Price(ticker='eth_usd', price=eth_usd),
    ]


async def _save_prices(prices: list[deribit.schema.Price]):
    for price in prices:
        await deribit.db.service.create_price(price)
