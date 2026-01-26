import logging
import unittest.mock

import pytest

import deribit

logger = logging.getLogger(__name__)

index_price = 11111.1
response_json = {
    "jsonrpc": "2.0",
    "result":
        {
            "estimated_delivery_price": 93151.18,
            "index_price": index_price
        },
    "usIn": 1768823460261169,
    "usOut": 1768823460261378,
    "usDiff": 209,
    "testnet": False
}

index_price2 = 22222.2
response_json2 = {
    **response_json,
    **{'result': {'index_price': index_price2}},
}


@pytest.fixture
def api_service():
    return deribit.api.FetchSerice()


@pytest.mark.anyio
async def test_deribit(api_service):

    with unittest.mock.patch.object(
            api_service.repository,
            'get',
            unittest.mock.AsyncMock(return_value=response_json)):
        assert await api_service.fetch_btc_usd_price() == index_price

    with unittest.mock.patch.object(
            api_service.repository,
            'get',
            unittest.mock.AsyncMock(return_value=response_json2)):
        assert await api_service.fetch_eth_usd_price() == index_price2
