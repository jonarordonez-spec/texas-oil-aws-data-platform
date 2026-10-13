
from pathlib import Path
import pandas as pd


# 1. File paths
SILVER_PATH = Path(
    "data/silver/county_production/county_production.parquet"
)

GOLD_PATH = Path(
    "data/gold/county_oil_production_annual.parquet"
)


# 2. Load Silver data
def load_silver_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Silver file not found: {path}"
        )

    df = pd.read_parquet(path)

    print(f"Silver rows loaded: {len(df):,}")

    return df


# 3. Transform Silver to Gold
def transform_to_gold(df: pd.DataFrame) -> pd.DataFrame:
    oil_df = df.loc[
        df["OIL_GAS_CODE"] == "O"
    ].copy()

    gold_df = (
        oil_df.groupby(
            ["COUNTY_NO", "CYCLE_YEAR"],
            as_index=False
        )
        .agg(
            annual_oil_production=(
                "CNTY_OIL_PROD_VOL",
                "sum"
            ),
            months_reported=(
                "CYCLE_MONTH",
                "nunique"
            )
        )
    )

    gold_df["has_12_months"] = (
        gold_df["months_reported"] == 12
    )

    return gold_df


# 4. Validate Gold data
def validate_gold(df: pd.DataFrame) -> None:
    keys = ["COUNTY_NO", "CYCLE_YEAR"]

    # Check null keys
    assert not df[keys].isna().any().any(), (
        "Gold contains null keys"
    )

    # Check duplicate county-year keys
    assert not df.duplicated(subset=keys).any(), (
        "Gold contains duplicate county-year keys"
    )

    # Check monthly coverage
    assert df["months_reported"].between(1, 12).all(), (
        "Invalid monthly coverage"
    )

    # Check null production values
    assert df["annual_oil_production"].notna().all(), (
        "Gold contains null production values"
    )

    # Check negative production values
    assert (df["annual_oil_production"] >= 0).all(), (
        "Gold contains negative production values"
    )

    # NEW: Check consistency of monthly coverage flag
    expected_flag = df["months_reported"] == 12

    if not df["has_12_months"].eq(expected_flag).all():
        raise ValueError(
            "Gold validation failed: has_12_months "
            "is inconsistent with months_reported"
        )

    print("Gold validation passed!")


# 5. Run pipeline
def main():
    silver_df = load_silver_data(SILVER_PATH)

    gold_df = transform_to_gold(silver_df)

    print(f"Gold rows created: {len(gold_df):,}")

    validate_gold(gold_df)

    # Save validated Gold data
    GOLD_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    gold_df.to_parquet(
        GOLD_PATH,
        index=False
    )

    print(f"\nGold saved to: {GOLD_PATH}")

    # Identify incomplete county-year observations
    partial_years = gold_df.loc[
        gold_df["months_reported"] < 12
    ]

    print("\nPartial coverage by year:")
    print(
        partial_years["CYCLE_YEAR"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    # Monthly coverage distribution
    print("\nMonthly coverage distribution:")
    print(
        gold_df["months_reported"]
        .value_counts()
        .sort_index()
    )

    # Show examples of incomplete observations
    print("\nExamples with fewer than 12 months:")
    print(
        partial_years[
            [
                "COUNTY_NO",
                "CYCLE_YEAR",
                "annual_oil_production",
                "months_reported",
            ]
        ].head(10).to_string(index=False)
    )

    # Preview Gold data
    print("\nFirst 10 Gold rows:")
    print(gold_df.head(10))


if __name__ == "__main__":
    main()
