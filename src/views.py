import os
import json
from datetime import datetime
from typing import Any

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_time_now() -> str:
    time = datetime.now()
    if 21 < time.hour <= 5:
        return "Доброй ночи"
    elif 5 < time.hour <= 10:
        return "Доброе утро"
    elif 10 < time.hour <= 17:
        return "Добрый день"
    elif 17 < time.hour <= 21:
        return "Добрый вечер"


def get_card_data(df: pd.DataFrame) -> list:
    """
    Extracts and processes card transaction data from a DataFrame.

    Parameters:
        df (DataFrame): Input DataFrame containing transaction data.

    Returns:
        List[Dict[str, str]]: List of dictionaries with card data.
    """
    df['Номер карты'] = df['Номер карты'].fillna('Unknown')
    df_total_spend = df[df['Сумма операции'] < 0].groupby('Номер карты').agg({
        'Сумма операции': 'sum',
        'Кэшбэк': 'sum'
    }).reset_index()

    return [
        {
            "last_digits": row["Номер карты"],
            "total_spent": row["Сумма операции"],
            "cashback": row["Кэшбэк"]
        }
        for idx, row in df_total_spend.iterrows()
    ]


def get_top_transactions_by_date(transactions: pd.DataFrame) -> str:
    transactions = transactions.to_dict('records')
    result = []
    transactions = sorted(transactions, key=lambda x: x["Сумма операции с округлением"], reverse=True)[:5]
    for transaction in transactions:
        result.append(
            {
                "date": transaction["Дата операции"],
                "amount": transaction["Сумма операции"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    return json.dumps(result, ensure_ascii=False, indent=4)


def get_current_exchange_rate(currency: list) -> str:
    # Получение актуального курса доллара и/или евро в рублях
    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base="
    headers = {"apikey": API_KEY}
    try:
        result = []
        for value in currency:
            response = requests.get(url + value, headers=headers).json()
            data = {"currency": value, "rate": float(response["rates"]["RUB"])}
            result.append(data)
        return json.dumps(result, ensure_ascii=False, indent=4)
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Error: {e}")
        return ''


def get_stock_currency(stock: str) -> Any:
    """Возвращает курс акций"""
    ticker = yf.Ticker(stock)
    data_today = ticker.history(period="1d")
    if not data_today.empty:
        high_price = data_today["High"].iloc[0]
        return high_price
    else:
        return 0.0


def main_page(df: pd.DataFrame) -> dict:
    result = {
        "greeting": get_time_now(),
        "cards": get_card_data(df),
        "top_transactions": get_top_transactions_by_date(df),
        "currency_rates": get_current_exchange_rate(["USD", "EUR"]),
        "stock_prices": [
            {"stock": "AAPL", "price": round(get_stock_currency("AAPL"), 2)},
            {"stock": "AMZN", "price": round(get_stock_currency("AMZN"), 2)},
            {"stock": "GOOGL", "price": round(get_stock_currency("GOOGL"), 2)},
            {"stock": "MSFT", "price": round(get_stock_currency("MSFT"), 2)},
            {"stock": "TSLA", "price": round(get_stock_currency("TSLA"), 2)},
        ],
    }

    return result
