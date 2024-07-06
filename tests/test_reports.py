import logging

import pandas as pd
import pytest
from pandas import DataFrame

from src.reports import spending_by_category

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def sample_transactions() -> DataFrame:
    """
    Fixture to create a sample DataFrame of transactions for testing.

    Returns:
        DataFrame: A DataFrame containing sample transaction data.
    """
    data = {
        'Дата операции': [
            '01.06.2023 08:00:00',
            '15.07.2023 12:00:00',
            '25.07.2023 18:00:00',
            '10.08.2023 10:00:00',
            '20.09.2023 09:00:00'
        ],
        'Категория': [
            'Рестораны',
            'Рестораны',
            'Кино',
            'Рестораны',
            'Рестораны'
        ]
    }
    df = pd.DataFrame(data)
    logger.info("Sample transactions DataFrame created.")
    return df


def test_spending_by_category_default_date(sample_transactions: DataFrame) -> None:
    """
    Test spending_by_category function with default date filter.

    Args:
        sample_transactions (DataFrame): The sample transactions DataFrame.
    """
    logger.info("Testing spending_by_category with default date filter.")
    result = spending_by_category(sample_transactions, "Рестораны")
    assert result.shape[0] == 0


def test_spending_by_category_custom_date(sample_transactions: DataFrame) -> None:
    """
    Test spending_by_category function with a custom date filter.

    Args:
        sample_transactions (DataFrame): The sample transactions DataFrame.
    """
    logger.info("Testing spending_by_category with custom date filter.")
    result = spending_by_category(sample_transactions, "Рестораны", date="20.08.2023")
    assert result.shape[0] == 3


def test_spending_by_category_no_results(sample_transactions: DataFrame) -> None:
    """
    Test spending_by_category function with a category that has no results.

    Args:
        sample_transactions (DataFrame): The sample transactions DataFrame.
    """
    logger.info("Testing spending_by_category with no results for category.")
    result = spending_by_category(sample_transactions, "Кино")
    assert result.empty


def test_spending_by_category_no_date_filter(sample_transactions: DataFrame) -> None:
    """
    Test spending_by_category function with no date filter.

    Args:
        sample_transactions (DataFrame): The sample transactions DataFrame.
    """
    logger.info("Testing spending_by_category with no date filter.")
    result = spending_by_category(sample_transactions, "Рестораны", date=None)
    assert result.shape[0] == 0


def test_spending_by_category_invalid_date_format(sample_transactions: DataFrame) -> None:
    """
    Test spending_by_category function with an invalid date format.

    Args:
        sample_transactions (DataFrame): The sample transactions DataFrame.
    """
    logger.info("Testing spending_by_category with invalid date format.")
    with pytest.raises(ValueError):
        spending_by_category(sample_transactions, "Рестораны", date="2023-08-20")