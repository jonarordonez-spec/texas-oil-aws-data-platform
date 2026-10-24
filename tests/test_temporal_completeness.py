
import pandas as pd

from src.transform_silver_to_gold import transform_to_gold


def test_full_year_has_twelve_months():
    """Verify that twelve distinct months produce a complete coverage flag."""

    # Arrange: Create twelve monthly oil production records.
    df = pd.DataFrame({
        "COUNTY_NO": [101] * 12,
        "CYCLE_YEAR": [2024] * 12,
        "CYCLE_MONTH": list(range(1, 13)),
        "OIL_GAS_CODE": ["O"] * 12,
        "CNTY_OIL_PROD_VOL": [1000] * 12,
    })

    # Act: Transform monthly Silver records into annual Gold data.
    gold_df = transform_to_gold(df)

    # Assert: Verify annual production and temporal coverage.
    assert len(gold_df) == 1
    assert gold_df.loc[0, "annual_oil_production"] == 12000
    assert gold_df.loc[0, "months_reported"] == 12
    assert bool(gold_df.loc[0, "has_12_months"]) is True


def test_partial_year_has_incomplete_coverage():
    """Verify that ten distinct months produce an incomplete coverage flag."""

    # Arrange: Create ten monthly oil production records.
    df = pd.DataFrame({
        "COUNTY_NO": [202] * 10,
        "CYCLE_YEAR": [2024] * 10,
        "CYCLE_MONTH": list(range(1, 11)),
        "OIL_GAS_CODE": ["O"] * 10,
        "CNTY_OIL_PROD_VOL": [1000] * 10,
    })

    # Act: Transform monthly Silver records into annual Gold data.
    gold_df = transform_to_gold(df)

    # Assert: Verify observed production and partial coverage.
    assert len(gold_df) == 1
    assert gold_df.loc[0, "annual_oil_production"] == 10000
    assert gold_df.loc[0, "months_reported"] == 10
    assert bool(gold_df.loc[0, "has_12_months"]) is False


def test_multiple_districts_do_not_increase_month_count():
    """Verify that multiple district records do not inflate monthly coverage."""

    # Arrange: Two districts report production in the same three months.
    df = pd.DataFrame({
        "COUNTY_NO": [101, 101, 101, 101, 101, 101],
        "DISTRICT_NO": [1, 2, 1, 2, 1, 2],
        "CYCLE_YEAR": [2024] * 6,
        "CYCLE_MONTH": [1, 1, 2, 2, 3, 3],
        "OIL_GAS_CODE": ["O"] * 6,
        "CNTY_OIL_PROD_VOL": [1000] * 6,
    })

    # Act: Aggregate district-level records into county-year data.
    gold_df = transform_to_gold(df)

    # Assert: All production is included, but only three months are counted.
    assert len(gold_df) == 1
    assert gold_df.loc[0, "annual_oil_production"] == 6000
    assert gold_df.loc[0, "months_reported"] == 3
    assert bool(gold_df.loc[0, "has_12_months"]) is False
