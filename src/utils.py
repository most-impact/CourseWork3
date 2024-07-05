import json
from typing import Any

import pandas as pd


def read_xls_file(filename: str) -> list[Any]:
    if filename.endswith(".xls"):
        data = pd.read_excel(filename)
        return data.to_dict("records")
    else:
        return []


def write_data_in_file(file: str, data: Any) -> None:
    with open(file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)
