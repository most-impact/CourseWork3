import json
import re
from typing import Any, Hashable

from src.utils import setup_logger

logger = setup_logger()


def simple_searching(searching_str: str, transactions: list[dict[Hashable, Any]], user_value) -> str:
    """Возвращает данные в json-формате необходимые для сервисов"""
    result = []
    if user_value == "1":
        for transaction in transactions:
            if re.search(searching_str.lower(), str(transaction["Категория"]).lower()):
                result.append(transaction)
    elif user_value == "2":
        for transaction in transactions:
            if re.search(searching_str.lower(), str(transaction["Описание"]).lower()):
                result.append(transaction)
    elif user_value == "3":
        for transaction in transactions:
            if re.search(searching_str.lower(), str(transaction["Описание"]).lower()) or re.search(
                searching_str.lower(), str(transaction["Категория"]).lower()
            ):
                result.append(transaction)
    else:
        print("Некорректный ответ")
        logger.info("Пользователь ввел некорректные данные в функции simple_searching")
        return simple_searching(searching_str, transactions, user_value)
    logger.error("Функция simple_searching выполнена успешно")
    return json.dumps(result, ensure_ascii=False, indent=4)
