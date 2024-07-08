import pandas as pd

from src.reports import spending_by_category


def test_filter_transactions_empty_result() -> None:
    transactions = pd.DataFrame(
        {
            "category": ["Переводы", "Переводы", "Супермаркеты"],
            "data_payment": ["01.01.2023", "15.01.2023", "08.07.2024"],
        }
    )

    filtered_transactions1 = spending_by_category(transactions, "Электроника", "01.01.2023")
    filtered_transactions2 = spending_by_category(transactions, "Переводы", "01.01.2023")
    filtered_transactions_without_data = spending_by_category(transactions, "Супермаркеты")

    assert len(filtered_transactions1) == 0
    assert len(filtered_transactions2) == 2
    assert len(filtered_transactions_without_data) == 1
