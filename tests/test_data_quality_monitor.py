
import pandas as pd
import pytest

from src.data_quality_monitor import calculate_quality_metrics


def test_calculate_quality_metrics():
    df = pd.DataFrame(
        {
            "CNTY_OIL_PROD_VOL": [100, 200, 0, None, 500]
        }
    )

    metrics = calculate_quality_metrics(df)

    assert metrics["row_count"] == 5
    assert metrics["null_production_count"] == 1
    assert metrics["null_rate"] == 20.0
    assert metrics["zero_production_count"] == 1
    assert metrics["zero_rate"] == 20.0


def test_empty_dataframe():
    df = pd.DataFrame(
        {
            "CNTY_OIL_PROD_VOL": pd.Series(dtype="float64")
        }
    )

    metrics = calculate_quality_metrics(df)

    assert metrics["row_count"] == 0
    assert metrics["null_production_count"] == 0
    assert metrics["null_rate"] == 0.0
    assert metrics["zero_production_count"] == 0
    assert metrics["zero_rate"] == 0.0

def test_missing_production_column():
    df = pd.DataFrame(
        {
            "COUNTY_NO": [1, 2, 3]
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required column"
    ):
        calculate_quality_metrics(df)