import json
from typing import Any, Hashable

import pytest

from src.services import simple_searching
from src.utils import setup_logger

logger = setup_logger()


@pytest.fixture
def sample_transactions() -> list[dict[Hashable, Any]]:
    return [
        {"Категория": "Еда", "Описание": "Покупка в магазине", "Сумма операции": -1500},
        {"Категория": "Переводы", "Описание": "С карты на карты", "Сумма операции": -2000},
        {"Категория": "Переводы", "Описание": "С карты на счет", "Сумма операции": -500},
    ]


def test_simple_searching(sample_transactions):
    result_1 = json.loads(simple_searching("карт", sample_transactions, "2"))
    assert result_1 == [
        {"Категория": "Переводы", "Описание": "С карты на карты", "Сумма операции": -2000},
        {"Категория": "Переводы", "Описание": "С карты на счет", "Сумма операции": -500},
    ]
    result_2 = json.loads(simple_searching("а", sample_transactions, "3"))
    assert result_2 == [
        {"Категория": "Еда", "Описание": "Покупка в магазине", "Сумма операции": -1500},
        {"Категория": "Переводы", "Описание": "С карты на карты", "Сумма операции": -2000},
        {"Категория": "Переводы", "Описание": "С карты на счет", "Сумма операции": -500},
    ]
