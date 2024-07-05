from datetime import timedelta
from typing import Any, Optional

import pandas as pd


def wastes_by_category(transactions: pd.DataFrame, category: str, date: Optional[pd.Timestamp] = None) -> Any:
    transactions = pd.DataFrame(transactions)
    if date is None:
        date = pd.to_datetime("today")
    else:
        date = pd.to_datetime(date)
    result: dict = {}
    three_months_ago = date - timedelta(days=90)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    total = -transactions[
        (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= date)
        & (transactions["Категория"] == category)
    ]["Сумма операции"]
    if total.any():
        result["amount"] = total.to_dict()
        result["category"] = category
        result["total"] = total.sum()

    return result
