
import pandas as pd


def calculate_quality_metrics(
    df: pd.DataFrame,
    production_column: str = "CNTY_OIL_PROD_VOL",
) -> dict:
    """Calculate basic data quality metrics for production data."""

    if production_column not in df.columns:
        raise ValueError(
            f"Missing required column: {production_column}"
        )

    row_count = len(df)

    null_count = int(df[production_column].isna().sum())
    zero_count = int(df[production_column].eq(0).sum())

    null_rate = (
        round(null_count / row_count * 100, 2)
        if row_count > 0
        else 0.0
    )

    zero_rate = (
        round(zero_count / row_count * 100, 2)
        if row_count > 0
        else 0.0
    )

    return {
        "row_count": row_count,
        "null_production_count": null_count,
        "null_rate": null_rate,
        "zero_production_count": zero_count,
        "zero_rate": zero_rate,
    }
