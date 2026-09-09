from pathlib import Path

import pandas as pd


BRONZE_FILE = Path(
    "data/bronze/county_production/county_production.parquet"
)

SILVER_DIR = Path(
    "data/silver/county_production"
)

SILVER_FILE = SILVER_DIR / "county_production.parquet"


def read_bronze_data(bronze_file: Path) -> pd.DataFrame:
    """Read the Bronze county production dataset."""
    return pd.read_parquet(bronze_file)


def validate_required_identifiers(df: pd.DataFrame) -> None:
    """Validate that required identifying fields contain no null values."""
    required_identifiers = [
        "COUNTY_NO",
        "DISTRICT_NO",
        "CYCLE_YEAR",
        "CYCLE_MONTH",
        "OIL_GAS_CODE",
    ]

    null_counts = df[required_identifiers].isna().sum()

    if (null_counts > 0).any():
        raise ValueError(
            f"Required identifiers contain null values:\n{null_counts}"
        )


def validate_month_range(df: pd.DataFrame) -> None:
    """Validate that cycle month is between 1 and 12."""
    invalid_months = ~df["CYCLE_MONTH"].between(1, 12)

    if invalid_months.any():
        raise ValueError(
            f"Invalid CYCLE_MONTH values found: "
            f"{df.loc[invalid_months, 'CYCLE_MONTH'].unique().tolist()}"
        )


def validate_candidate_key(df: pd.DataFrame) -> None:
    """Validate that the candidate key is unique."""
    candidate_key = [
        "COUNTY_NO",
        "DISTRICT_NO",
        "CYCLE_YEAR",
        "CYCLE_MONTH",
        "OIL_GAS_CODE",
    ]

    duplicate_keys = df.duplicated(
        subset=candidate_key,
        keep=False,
    )

    if duplicate_keys.any():
        raise ValueError(
            f"Duplicate candidate keys found: {duplicate_keys.sum()}"
        )


def validate_contract(df: pd.DataFrame) -> None:
    """Validate the Silver data contract."""
    validate_required_identifiers(df)
    validate_month_range(df)
    validate_candidate_key(df)


def write_silver_data(df: pd.DataFrame, silver_file: Path) -> None:
    """Write validated data to the Silver layer."""
    silver_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(silver_file, engine="pyarrow", index=False)


def main() -> None:
    df = read_bronze_data(BRONZE_FILE)

    validate_contract(df)

    write_silver_data(df, SILVER_FILE)

    print(f"Rows processed: {len(df):,}")
    print("Silver contract validation: PASSED")
    print(f"Output: {SILVER_FILE}")


if __name__ == "__main__":
    main()