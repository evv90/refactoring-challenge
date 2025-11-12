# noqa: PLR2004; allow "magic numbers" in tests
"""Tests for waqupy.utils module."""
import pytest

from waqupy.utils import parse_date


# AI-ASSIST: AI wrote most of this test
def test_parse_date() -> None:
    """Test the parse_date function with various formats and invalid inputs."""
    d1 = parse_date("2024-01-03")
    assert d1.year == 2024
    assert d1.month == 1
    assert d1.day == 3

    d2 = parse_date("2024/01/03")
    assert d2.year == 2024
    assert d2.month == 1
    assert d2.day == 3

    # Manual correction: added invalid date formats; added more specific error matching
    with pytest.raises(ValueError, match="Invalid isoformat string"):
        parse_date("24-01-03")  # invalid date: YY-MM-DD
    with pytest.raises(ValueError, match="Invalid isoformat string"):
        parse_date("2024-29-12 ")  # invalid date: YYYY-DD-MM
