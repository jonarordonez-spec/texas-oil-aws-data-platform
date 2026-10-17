import pandas as pd
import pytest

from src.transform_silver_to_gold import validate_gold


def test_gold_rejects_negative_production():
    # Arrange: create intentionally invalid Gold data
    gold = pd.DataFrame({
        "COUNTY_NO": [5],
        "CYCLE_YEAR": [2024],
        "annual_oil_production": [-150],
        "months_reported": [12],
        "has_12_months": [True],
    })

    # Act and Assert: validation must reject negative production
    with pytest.raises(
        AssertionError,
        match="Gold contains negative production values"
    ):
        validate_gold(gold)