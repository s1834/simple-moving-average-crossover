import pytest
import pandas as pd

def test_data():
    data = pd.read_csv('hindalco.csv', parse_dates=['datetime'])
    for index, row in data.iterrows():
        assert isinstance(row['open'], float)
        assert isinstance(row['high'], float)
        assert isinstance(row['low'], float)
        assert isinstance(row['close'], float)
        assert isinstance(row['volume'], int)
        assert isinstance(row['instrument'], str)
        assert isinstance(row['datetime'], pd.Timestamp)