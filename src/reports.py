from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.utils import setup_logger

logger = setup_logger()


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает данные в json-формате необходимые для главной страницы"""
    if date is None:
        date = datetime.now().strftime("%d.%m.%Y")
    end_date = datetime.strptime(date, "%d.%m.%Y") - timedelta(days=90)
    filtered_transactions = transactions[
        (transactions["category"] == category)
        & (transactions["data_payment"] >= date)
        & (transactions["data_payment"] < end_date.strftime("d.%m.%Y"))
    ]
    logger.error("Функция spending_by_category выполнена успешно")
    return filtered_transactions
