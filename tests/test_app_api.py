import unittest.mock

import fastapi.testclient
import pytest

import app

last_price = {
    "ticker": "btc_usd",
    "price": 88398.52,
    "timestamp": 1769342862,
}


@pytest.fixture
def client():
    return fastapi.testclient.TestClient(app.app)


@pytest.mark.anyio
async def test_price_endpoints(client):

    class MockRepo:
        async def iter_prices(self, *args, **kwargs):
            yield last_price
            yield last_price

    # Подменяем репозиторий на мок
    with unittest.mock.patch(
            'deribit.db.DbService.repository_cls',
            new=MockRepo):

        result = client.get('/prices/last?ticker=btc_usd')
        assert result.status_code == 200
        assert result.json() == last_price

        result = client.get('/prices/?ticker=btc_usd')
        assert result.status_code == 200
        assert result.json() == [last_price, last_price]

        # Поскольку фильтрация по дате (`?date=2026-01-25`)
        # происходит в запросе к БД, а БД нет, то `date` не проверяем
