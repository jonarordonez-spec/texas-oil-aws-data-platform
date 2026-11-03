
import pytest

from src.compare_quality_baseline import compare_quality_metrics


def test_zero_rate_within_threshold():
    """A small change should not trigger an alert."""
    baseline = {
        "row_count": 129422,
        "null_rate": 0.0,
        "zero_rate": 12.1,
    }

    current = {
        "row_count": 129422,
        "null_rate": 0.0,
        "zero_rate": 15.0,
    }

    result = compare_quality_metrics(baseline, current)

    assert result["zero_rate_change_pp"] == 2.9
    assert result["threshold_exceeded"] is False
    assert result["status"] == "WITHIN_THRESHOLD"


def test_zero_rate_increase_triggers_alert():
    """A large increase should trigger an alert."""
    baseline = {
        "row_count": 129422,
        "null_rate": 0.0,
        "zero_rate": 12.1,
    }

    current = {
        "row_count": 129422,
        "null_rate": 0.0,
        "zero_rate": 25.0,
    }

    result = compare_quality_metrics(baseline, current)

    assert result["zero_rate_change_pp"] == 12.9
    assert result["threshold_exceeded"] is True
    assert result["status"] == "INVESTIGATE"


def test_zero_rate_decrease_triggers_alert():
    """A large decrease should also trigger an alert."""
    baseline = {
        "row_count": 129422,
        "null_rate": 0.0,
        "zero_rate": 12.1,
    }

    current = {
        "row_count": 129422,
        "null_rate": 0.0,
        "zero_rate": 3.0,
    }

    result = compare_quality_metrics(baseline, current)

    assert result["zero_rate_change_pp"] == -9.1
    assert result["threshold_exceeded"] is True
    assert result["status"] == "INVESTIGATE"


def test_negative_threshold_fails():
    """A negative threshold should be rejected."""
    baseline = {
        "row_count": 129422,
        "null_rate": 0.0,
        "zero_rate": 12.1,
    }

    with pytest.raises(ValueError):
        compare_quality_metrics(
            baseline,
            baseline,
            threshold_pp=-5.0,
        )
