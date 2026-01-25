import unittest.mock

import fastapi.testclient
import pytest

import app


last_price = {
    "ticker": "btc_usd",
    "price": 88398.52,
    "timestamp": 1769342862,
    "timestamp_as_dt": "2026-01-25 12:07:42"
}


@pytest.fixture
def client():
    return fastapi.testclient.TestClient(app.app)


@pytest.mark.anyio
async def test__get_last_price(client):
    pass
    # repo_mock = unittest.mock.AsyncMock()
    # assert True
