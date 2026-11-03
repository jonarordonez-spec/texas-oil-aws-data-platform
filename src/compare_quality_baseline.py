
import json
from pathlib import Path


BASELINE_PATH = Path("reports/silver_oil_quality_baseline.json")
REPORT_PATH = Path("reports/silver_oil_quality_report.json")

ZERO_RATE_THRESHOLD_PP = 5.0


def load_json(file_path: Path) -> dict:
    """Load a JSON file."""
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def compare_quality_metrics(
    baseline: dict,
    current: dict,
    threshold_pp: float = ZERO_RATE_THRESHOLD_PP,
) -> dict:
    """Compare current quality metrics against a baseline."""
    if threshold_pp < 0:
        raise ValueError("Threshold must be non-negative.")

    required_metrics = {"zero_rate", "null_rate", "row_count"}

    for name, metrics in [
        ("baseline", baseline),
        ("current", current),
    ]:
        missing = required_metrics - set(metrics)

        if missing:
            raise ValueError(
                f"Missing metrics in {name}: {sorted(missing)}"
            )

    zero_rate_change_pp = round(
        current["zero_rate"] - baseline["zero_rate"], 2
    )

    threshold_exceeded = (
        abs(zero_rate_change_pp) > threshold_pp
    )

    return {
        "baseline_zero_rate": baseline["zero_rate"],
        "current_zero_rate": current["zero_rate"],
        "zero_rate_change_pp": zero_rate_change_pp,
        "threshold_pp": threshold_pp,
        "threshold_exceeded": threshold_exceeded,
        "status": (
            "INVESTIGATE"
            if threshold_exceeded
            else "WITHIN_THRESHOLD"
        ),
    }


def main() -> None:
    """Compare the latest quality report against the baseline."""
    baseline = load_json(BASELINE_PATH)
    report = load_json(REPORT_PATH)

    current_metrics = report["metrics"]

    comparison = compare_quality_metrics(
        baseline,
        current_metrics,
    )

    print(json.dumps(comparison, indent=4))


if __name__ == "__main__":
    main()
