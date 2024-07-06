import pandas as pd
import pytest
from unittest.mock import patch, mock_open
from src.utils import read_xls_file


# Мок для pd.read_excel
@patch("pandas.read_excel")
def test_read_xls_file(mock_read_excel):
    mock_data = pd.DataFrame({
        "Колонка1": [1, 2, 3],
        "Колонка2": ["а", "б", "в"]
    })
    mock_read_excel.return_value = mock_data

    filename = "mocked_file.xlsx"
    df = read_xls_file(filename)

    mock_read_excel.assert_called_once_with(filename)
    assert not df.empty
    assert list(df.columns) == ["Колонка1", "Колонка2"]
    assert df.shape == (3, 2)
    assert df["Колонка1"].tolist() == [1, 2, 3]
    assert df["Колонка2"].tolist() == ["а", "б", "в"]