import json
from typing import Any

import pandas as pd


def read_xls_file(filename: str) -> pd.DataFrame:
    data = pd.read_excel(filename)
    return data
