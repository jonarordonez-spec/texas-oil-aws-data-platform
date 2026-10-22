
import pandas as pd
import pytest

from src.transform_bronze_to_silver import validate_numeric_columns


def test_integer_production_passes():
    """Accept production values stored as integers."""
    df = pd.DataFrame({
        "CNTY_OIL_PROD_VOL": [1500, 2300],
    })

    validate_numeric_columns(df)


def test_text_production_fails():
    """Reject production values stored as text."""
    df = pd.DataFrame({
        "CNTY_OIL_PROD_VOL": ["1500", "2300"],
    })

    with pytest.raises(
        ValueError,
        match="CNTY_OIL_PROD_VOL must be numeric",
    ):
        validate_numeric_columns(df)


def test_pyarrow_integer_production_passes():
    """Accept Arrow-backed integer production values."""
    df = pd.DataFrame({
        "CNTY_OIL_PROD_VOL": pd.Series(
            [1500, 2300],
            dtype="int64[pyarrow]",
        ),
    })

    validate_numeric_columns(df)
