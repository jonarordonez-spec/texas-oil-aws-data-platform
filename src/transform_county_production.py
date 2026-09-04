from pathlib import Path

import pandas as pd


SOURCE_FILE = Path(
    r"C:\proyectos\texas-oil-gas-analytics\github-oil-gas-texas"
    r"\data\raw\OG_COUNTY_CYCLE_DATA_TABLE.dsv"
)

OUTPUT_DIR = Path("data/silver/county_production")
OUTPUT_FILE = OUTPUT_DIR / "county_production.parquet"


def read_raw_data(source_file: Path) -> pd.DataFrame:
    """Read the original RRC county production file."""
    return pd.read_csv(
        source_file,
        sep="}",
        dtype_backend="pyarrow",
    )


def validate_data(df: pd.DataFrame) -> None:
    """Validate basic expectations before writing Silver data."""
    required_columns = {
        "COUNTY_NO",
        "CYCLE_YEAR",
        "CYCLE_MONTH",
        "CNTY_OIL_PROD_VOL",
        "CNTY_GAS_PROD_VOL",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df.empty:
        raise ValueError("Dataset is empty")


def write_parquet(df: pd.DataFrame, output_file: Path) -> None:
    """Write the validated dataset as Parquet."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        output_file,
        engine="pyarrow",
        index=False,
    )


def main() -> None:
    df = read_raw_data(SOURCE_FILE)

    validate_data(df)

    write_parquet(df, OUTPUT_FILE)

    print(f"Rows processed: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()