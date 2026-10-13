
import pandas as pd
import pytest

from src.transform_silver_to_gold import (
    transform_to_gold,
    validate_gold,
)

def test_gold_aggregation():
    silver = pd.DataFrame({
        "COUNTY_NO": [5, 5, 5, 5],
        "CYCLE_YEAR": [2013, 2013, 2013, 2013],
        "CYCLE_MONTH": [1, 2, 3, 1],
        "OIL_GAS_CODE": ["O", "O", "O", "G"],
        "CNTY_OIL_PROD_VOL": [100, 200, 0, 999],
    })

    gold = transform_to_gold(silver)

    assert len(gold) == 1
    assert gold.iloc[0]["annual_oil_production"] == 300
    assert gold.iloc[0]["months_reported"] == 3

def test_gold_rejects_duplicate_keys():
    gold = pd.DataFrame({
        "COUNTY_NO": [5, 5],
        "CYCLE_YEAR": [2013, 2013],
        "annual_oil_production": [100, 200],
        "months_reported": [12, 12],
    })

    try:
        validate_gold(gold)
    except AssertionError as error:
        assert "duplicate" in str(error)
    else:
        raise AssertionError(
            "Validation should reject duplicate keys"
        )

def test_gold_preserves_zero_production():
    silver = pd.DataFrame({
        "COUNTY_NO": [5, 5],
        "CYCLE_YEAR": [2013, 2013],
        "CYCLE_MONTH": [1, 2],
        "OIL_GAS_CODE": ["O", "O"],
        "CNTY_OIL_PROD_VOL": [0, 0],
    })

    gold = transform_to_gold(silver)

    assert gold.iloc[0]["annual_oil_production"] == 0
    assert gold.iloc[0]["months_reported"] == 2

def test_gold_monthly_coverage_flag():
    silver = pd.DataFrame({
        "COUNTY_NO": [1, 1, 2],
        "CYCLE_YEAR": [2025, 2025, 2025],
        "CYCLE_MONTH": [1, 2, 1],
        "OIL_GAS_CODE": ["O", "O", "O"],
        "CNTY_OIL_PROD_VOL": [100, 200, 50],
    })

    gold = transform_to_gold(silver)

    assert gold["has_12_months"].eq(
        gold["months_reported"] == 12
    ).all()

    assert not gold["has_12_months"].any()

def test_gold_full_coverage_flag():
    months = list(range(1, 13))

    silver = pd.DataFrame({
        "COUNTY_NO": [5] * 12,
        "CYCLE_YEAR": [2024] * 12,
        "CYCLE_MONTH": months,
        "OIL_GAS_CODE": ["O"] * 12,
        "CNTY_OIL_PROD_VOL": [100] * 12,
    })

    gold = transform_to_gold(silver)

    assert len(gold) == 1
    assert gold.iloc[0]["months_reported"] == 12
    assert gold.iloc[0]["has_12_months"]
    assert gold.iloc[0]["annual_oil_production"] == 1200

def test_gold_rejects_inconsistent_coverage_flag():
    gold = pd.DataFrame({
        "COUNTY_NO": [5],
        "CYCLE_YEAR": [2024],
        "annual_oil_production": [1200],
        "months_reported": [12],
        "has_12_months": [False],
    })

    with pytest.raises(
        ValueError,
        match="has_12_months is inconsistent"
    ):
        validate_gold(gold)
