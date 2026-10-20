
import pandas as pd
import pytest

from src.transform_bronze_to_silver import validate_contract


def test_missing_required_column_fails():
    # ARRANGE: Dataset missing the oil production column.
    test_data = pd.DataFrame(
        {
            "COUNTY_NO": [101],
            "DISTRICT_NO": [8],
            "CYCLE_YEAR": [2026],
            "CYCLE_MONTH": [3],
            "OIL_GAS_CODE": ["O"],
        }
    )

    # ACT & ASSERT: Missing column must raise an error.
    with pytest.raises(
        ValueError,
        match="Missing required columns.*CNTY_OIL_PROD_VOL",
    ):
        validate_contract(test_data)


def test_valid_schema_passes():
    # ARRANGE: Dataset containing all required columns.
    test_data = pd.DataFrame(
        {
            "COUNTY_NO": [101],
            "DISTRICT_NO": [8],
            "CYCLE_YEAR": [2026],
            "CYCLE_MONTH": [3],
            "OIL_GAS_CODE": ["O"],
            "CNTY_OIL_PROD_VOL": [1500],
        }
    )

    # ACT & ASSERT: Validation should finish without errors.
    validate_contract(test_data)
