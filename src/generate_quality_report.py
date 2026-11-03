
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.data_quality_monitor import calculate_quality_metrics


SOURCE_PATH = Path(
    "data/silver/county_production/county_production.parquet"
)
REPORT_PATH = Path("reports/silver_oil_quality_report.json")

OIL_GAS_COLUMN = "OIL_GAS_CODE"
OIL_CODE = "O"
PRODUCTION_COLUMN = "CNTY_OIL_PROD_VOL"


def calculate_file_hash(file_path: Path) -> str:
    """Calculate the SHA-256 hash of a file."""
    hasher = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def get_git_metadata() -> dict:
    """Retrieve Git commit and working tree status."""
    commit = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    return {
        "git_commit": commit,
        "working_tree_clean": status == "",
    }


def generate_report() -> dict:
    """Generate a quality report for Silver oil production data."""
    if not SOURCE_PATH.is_file():
        raise FileNotFoundError(
            f"Source file not found: {SOURCE_PATH}"
        )

    df = pd.read_parquet(SOURCE_PATH)

    required_columns = {
        OIL_GAS_COLUMN,
        PRODUCTION_COLUMN,
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    oil_df = df.loc[df[OIL_GAS_COLUMN] == OIL_CODE]

    if oil_df.empty:
        raise ValueError("No oil production records found.")

    metrics = calculate_quality_metrics(
        oil_df,
        production_column=PRODUCTION_COLUMN,
    )

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_file": SOURCE_PATH.as_posix(),
        "source_sha256": calculate_file_hash(SOURCE_PATH),
        **get_git_metadata(),
        "metrics": metrics,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return report


if __name__ == "__main__":
    report = generate_report()

    print("Data quality report generated successfully.")
    print(f"Source: {report['source_file']}")
    print(f"Rows: {report['metrics']['row_count']}")
    print(f"SHA-256: {report['source_sha256']}")
    print(f"Report saved to: {REPORT_PATH}")
