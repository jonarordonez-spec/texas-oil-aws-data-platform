def test_ci_failure_demo():
    expected = 100
    actual = 90

    assert actual == expected, "CI demo: production does not match expected value"
