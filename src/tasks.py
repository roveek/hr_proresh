import celery


@celery.shared_task
def fetch_prices():
    ...


async def _fetch_prices():
    import deribit

    btc_usd = await deribit.fetch.btc_usd()
    eth_usd = await deribit.fetch.eth_usd()
