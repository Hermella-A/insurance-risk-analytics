import pytest
import pandas as pd
from src.eda_utils import load_data, basic_quality_report

def test_load_data(tmp_path):
    # Create a dummy CSV
    dummy = tmp_path / "dummy.csv"
    dummy.write_text("a,b\n1,2\n3,4")
    df = load_data(str(dummy))
    assert df.shape == (2, 2)

def test_basic_quality_report(capsys):
    df = pd.DataFrame({'col': [1,2,None]})
    basic_quality_report(df)
    captured = capsys.readouterr()
    assert "Missing values" in captured.out