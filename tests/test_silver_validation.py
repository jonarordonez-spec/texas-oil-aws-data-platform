import pandas as pd
import pytest

from src.transform_bronze_to_silver import (
    validate_candidate_key,
    validate_month_range,
    validate_required_identifiers,
)


def test_invalid_month_fails() -> None:
    test_data = pd.DataFrame(
        {
            "CYCLE_MONTH": [1, 6, 12, 15],
        }
    )

    with pytest.raises(ValueError):
        validate_month_range(test_data)


def test_null_identifier_fails() -> None:
    test_data = pd.DataFrame(
        {
            "COUNTY_NO": [101, None],
            "DISTRICT_NO": [8, 8],
            "CYCLE_YEAR": [2026, 2026],
            "CYCLE_MONTH": [3, 4],
            "OIL_GAS_CODE": ["O", "G"],
        }
    )

    with pytest.raises(ValueError):
        validate_required_identifiers(test_data)


def test_duplicate_candidate_key_fails() -> None:
    test_data = pd.DataFrame(
        {
            "COUNTY_NO": [101, 101],
            "DISTRICT_NO": [8, 8],
            "CYCLE_YEAR": [2026, 2026],
            "CYCLE_MONTH": [3, 3],
            "OIL_GAS_CODE": ["O", "O"],
        }
    )

    with pytest.raises(ValueError):
        validate_candidate_key(test_data)


def test_valid_data_passes() -> None:
    test_data = pd.DataFrame(
        {
            "COUNTY_NO": [101, 102],
            "DISTRICT_NO": [8, 8],
            "CYCLE_YEAR": [2026, 2026],
            "CYCLE_MONTH": [3, 4],
            "OIL_GAS_CODE": ["O", "G"],
        }
    )

    validate_required_identifiers(test_data)
    validate_month_range(test_data)
    validate_candidate_key(test_data)