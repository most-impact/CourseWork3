from src.reports import spending_by_category
from src.services import simple_searching
from src.utils import read_xls_file
from src.views import main_page


def main() -> None:
    """Отвечает за основную логику проекта с пользователем"""
    df = read_xls_file("../data/operations.xls")
    main_page(df)
    user_searching_str = input("Введите текст, который хотите найти: \n")
    user_value = input("Хотите провести поиск по: 1.Категории, 2.Описанию, 3. По обоим пунктам\n")
    simple_searching(user_searching_str, df.to_dict("records"), user_value)
    user_category = input("Введите категорию, по которой нужно провести поиск трат за последние 3 месяца\n")
    spending_by_category(df, user_category)


if __name__ == "__main__":
    main()
