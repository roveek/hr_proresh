import unittest.mock

import pytest

import deribit

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


@pytest.mark.anyio
async def test_deribit():

    with unittest.mock.patch('deribit.fetch._get',
                             unittest.mock.AsyncMock(
                                 return_value=response_json)):
        assert await deribit.fetch.btc_usd() == index_price

    with unittest.mock.patch('deribit.fetch._get',
                             unittest.mock.AsyncMock(
                                 return_value=response_json2)):
        assert await deribit.fetch.eth_usd() == index_price2
