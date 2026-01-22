import celery
import loguru

import deribit


@celery.shared_task
def fetch_prices():
    loguru.logger.info('Fetching prices task')
    # asyncio.run(_fetch_prices())
    return 'OK'


async def _fetch_prices():
    btc_usd = await deribit.fetch.btc_usd()
    loguru.logger.info(f'Fetched {btc_usd=}')

    eth_usd = await deribit.fetch.eth_usd()
    loguru.logger.info(f'Fetched {eth_usd=}')
