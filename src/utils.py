import logging

import pandas as pd


def setup_logger() -> logging.Logger:
    """Настройка логгера"""
    logger = logging.getLogger(__name__)

    file_handler = logging.FileHandler("logger.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s, %(module)s, %(levelname)s, %(message)s"))
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)
    return logger


def read_xls_file(filename: str) -> pd.DataFrame:
    """Функция для чтения Excel-файлов, возвращает DataFrame"""
    try:
        data = pd.read_excel(filename)
        return data
    except FileNotFoundError:
        setup_logger().error(f"Файл {filename} не найден")
        return pd.DataFrame()
