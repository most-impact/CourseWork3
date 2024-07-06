import re


def simple_searching(searching_str: str, transactions: dict):
    print("По какому значению вы хотите провести поиск?")
    user_value = input("1. По категории \n2. По описанию\n")
    print("Поиск по запросу:")
    result = []
    if user_value == "1":
        for transaction in transactions:
            if re.search(searching_str.lower(), str(transaction["Категория"]).lower()):
                result.append(transaction)
    elif user_value == "2":
        for transaction in transactions:
            if re.search(searching_str.lower(), str(transaction["Описание"]).lower()):
                result.append(transaction)
    else:
        print("Некорректный ответ")
        return simple_searching(searching_str, transactions)
    return result
