import json
import pytest
import pandas as pd
from unittest.mock import patch
from src.views import (
    get_time_now,
    get_card_data,
    get_top_transactions_by_date,
    get_stock_currency,
    main_page,
)


def test_get_time_now():
    assert isinstance(get_time_now(), str)


@pytest.fixture
def sample_transactions():
    return [
        {
            "Дата операции": "2023-05-01",
            "Номер карты": "1234",
            "Сумма операции": -1500,
            "Сумма операции с округлением": -1500,
            "Категория": "Продукты",
            "Описание": "Покупка в магазине",
        },
        {
            "Дата операции": "2023-05-02",
            "Номер карты": "5678",
            "Сумма операции": -2000,
            "Сумма операции с округлением": -2000,
            "Категория": "Развлечения",
            "Описание": "Посещение кинотеатра",
        },
    ]


@pytest.fixture
def sample_dataframe(sample_transactions):
    return pd.DataFrame(sample_transactions)


@pytest.fixture
def sample_df():
    data = {
        "Номер карты": ["1234", "5678", "1234", "5678", "1234", None],
        "Сумма операции": [-1000, -2000, -1500, 3000, -500, -1000],
        "Кэшбэк": [10, 20, 15, 0, 5, 10]
    }
    df = pd.DataFrame(data)
    return df


@patch("yfinance.Ticker.history")
def test_get_stock_currency(mock_history):
    mock_history.return_value = pd.DataFrame({"High": [150.0]})

    result = get_stock_currency("AAPL")
    assert result == 150.0

    mock_history.assert_called_once_with(period="1d")


def test_get_card_data(sample_df):
    expected = [
        {"last_digits": "1234", "total_spent": -3000, "cashback": 30},
        {"last_digits": "5678", "total_spent": -2000, "cashback": 20},
        {"last_digits": "Unknown", "total_spent": -1000, "cashback": 10}
    ]

    result = get_card_data(sample_df)
    assert result == expected


def test_get_top_transactions_by_date(sample_transactions):
    result = get_top_transactions_by_date(sample_transactions)
    expected = json.dumps(
        sorted(
            [
                {
                    "date": "2023-05-02",
                    "amount": -2000,
                    "category": "Развлечения",
                    "description": "Посещение кинотеатра",
                },
                {
                    "date": "2023-05-01",
                    "amount": -1500,
                    "category": "Продукты",
                    "description": "Покупка в магазине",
                },
            ],
            key=lambda x: x["amount"],
            reverse=True,
        ),
        ensure_ascii=False,
        indent=4,
    )
    assert result == expected


@patch("src.utils.get_time_now", return_value="Доброе утро")
@patch("src.utils.get_current_exchange_rate",
       return_value='[{"currency": "USD", "rate": 75.0}, {"currency": "EUR", "rate": 85.0}]')
@patch("src.utils.get_stock_currency")
def test_main_page(mock_get_stock_currency, sample_dataframe):
    mock_get_stock_currency.side_effect = [150.0, 200.0, 250.0, 300.0, 350.0]

    result = main_page(sample_dataframe)

    expected = {
        "greeting": "Доброе утро",
        "cards": json.dumps(
            [
                {
                    "last_digits": "1234",
                    "total_spent": 1500,
                    "cashback": -15.0,
                }
            ],
            ensure_ascii=False,
            indent=4,
        ),
        "top_transactions": json.dumps(
            [
                {
                    "date": "2023-05-02",
                    "amount": -2000,
                    "category": "Развлечения",
                    "description": "Посещение кинотеатра",
                },
                {
                    "date": "2023-05-01",
                    "amount": -1500,
                    "category": "Продукты",
                    "description": "Покупка в магазине",
                },
            ],
            ensure_ascii=False,
            indent=4,
        ),
        "currency_rates": '[{"currency": "USD", "rate": 75.0}, {"currency": "EUR", "rate": 85.0}]',
        "stock_prices": [
            {"stock": "AAPL", "price": 150.0},
            {"stock": "AMZN", "price": 200.0},
            {"stock": "GOOGL", "price": 250.0},
            {"stock": "MSFT", "price": 300.0},
            {"stock": "TSLA", "price": 350.0},
        ],
    }

    assert result == expected
