import json

from src.reports import spending_by_category
from src.services import simple_searching
from src.utils import read_xls_file
from src.views import main_page


def main() -> None:
    """
    The main function that reads transaction data, processes it, and prints the results.
    """
    df = read_xls_file("../data/operations.xls")
    data = main_page(df)

    print("Главная страница:")
    print(data)
    print()

    result = simple_searching(input('По какому ключевому слово вы хотите провести поиск'), data)

    category = input("Введите название категории: ")
    category_spending = spending_by_category(df, category).to_dict(orient='records')

    print("Траты по категории:")
    print(json.dumps(category_spending, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
