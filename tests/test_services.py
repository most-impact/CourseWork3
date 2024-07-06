import pytest
from unittest.mock import patch
from src.services import simple_searching

transactions = [
    {"Категория": "Продукты", "Описание": "Покупка в супермаркете"},
    {"Категория": "Транспорт", "Описание": "Проезд на автобусе"},
    {"Категория": "Развлечения", "Описание": "Посещение кинотеатра"},
]


@patch('builtins.input', side_effect=["1"])
def test_simple_searching_category(mock_input):
    result = simple_searching("продукты", transactions)
    assert len(result) == 1
    assert result[0]["Категория"] == "Продукты"


@patch('builtins.input', side_effect=["2"])
def test_simple_searching_description(mock_input):
    result = simple_searching("кинотеатра", transactions)
    assert len(result) == 1
    assert result[0]["Описание"] == "Посещение кинотеатра"


@patch('builtins.input', side_effect=["3"])
def test_simple_searching_invalid_input(mock_input):
    result = simple_searching("продукты", transactions)
    assert result == []