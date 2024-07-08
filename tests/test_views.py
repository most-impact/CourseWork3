import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from freezegun import freeze_time

from src.utils import setup_logger
from src.views import (
    get_card_data,
    get_current_exchange_rate,
    get_stock_currency,
    get_time_now,
    get_top_transactions_by_date,
)

logger = setup_logger()


@pytest.fixture
def sample_dataframe():
    data = {
        "Дата операции": [
            "2023-06-01 08:00:00",
            "2023-07-15 12:00:00",
            "2023-07-25 18:00:00",
            "2023-08-10 10:00:00",
            "2023-09-20 09:00:00",
        ],
        "Категория": ["Рестораны", "Рестораны", "Кино", "Рестораны", "Рестораны"],
        "Описание": ["Ужин", "Обед", "Фильм", "Завтрак", "Ужин"],
        "Сумма операции": [-1500, -2000, -500, -700, -900],
        "Сумма операции с округлением": [-1500, -2000, -500, -700, -900],
        "Кэшбэк": [50, 100, 20, 30, 40],
        "Номер карты": ["1234", "5678", "1234", "5678", "1234"],
    }
    return pd.DataFrame(data)


def test_get_time_now_morning():
    with freeze_time("2023-07-01 10:00:00"):
        assert get_time_now() == "Доброе утро"


def test_get_card_data(sample_dataframe):
    result = get_card_data(sample_dataframe)
    expected_result = json.dumps(
        [
            {"last_digits": "1234", "total_spent": -2900, "cashback": 110},
            {"last_digits": "5678", "total_spent": -2700, "cashback": 130},
        ],
        ensure_ascii=False,
        indent=4,
    )
    assert result == expected_result


def test_get_top_transactions_by_date(sample_dataframe):
    result = get_top_transactions_by_date(sample_dataframe)
    expected_result = json.dumps(
        [
            {"date": "2023-07-25 18:00:00", "amount": -500, "category": "Кино", "description": "Фильм"},
            {"date": "2023-08-10 10:00:00", "amount": -700, "category": "Рестораны", "description": "Завтрак"},
            {"date": "2023-09-20 09:00:00", "amount": -900, "category": "Рестораны", "description": "Ужин"},
            {"date": "2023-06-01 08:00:00", "amount": -1500, "category": "Рестораны", "description": "Ужин"},
            {"date": "2023-07-15 12:00:00", "amount": -2000, "category": "Рестораны", "description": "Обед"},
        ],
        ensure_ascii=False,
        indent=4,
    )
    assert result == expected_result


@patch("requests.get")
def test_get_current_exchange_rate(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"RUB": 75.0}}
    mock_get.return_value = mock_response

    result = get_current_exchange_rate(["USD"])
    expected_result = json.dumps([{"currency": "USD", "rate": 75.0}], ensure_ascii=False, indent=4)
    assert result == expected_result


@patch("yfinance.Ticker")
def test_get_stock_currency(mock_ticker):
    mock_history = MagicMock()
    mock_history.history.return_value = pd.DataFrame({"High": [150.0]})
    mock_ticker.return_value = mock_history

    result = get_stock_currency("AAPL")
    assert result == 150.0
