# ruff: noqa: PLR2004 - allow "magic numbers" in tests
"""Tests for waqupy.utils module."""

import textwrap
from typing import TYPE_CHECKING

import pytest

from waqupy.utils import parse_date, read_csv_as_dicts

if TYPE_CHECKING:
    from pathlib import Path


# AI-ASSIST: AI wrote most of this test.
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


# AI-ASSIST: AI wrote this test.
def test_read_csv_as_dicts(tmp_path: Path) -> None:
    """Test the read_csv_as_dicts function with a sample CSV file."""
    csv_content = textwrap.dedent(
        """\
        date, precip_mm, et_mm, tracer_upstream_mgL
        2024-01-01, 10.0, 2.0, 5.0
        2024-01-02, 0.0, 3.0, 4.5
        """
    )
    csv_path = tmp_path / "forcing.csv"
    csv_path.write_text(csv_content, encoding="utf-8")
    rows = read_csv_as_dicts(csv_path)
    assert len(rows) == 2
    assert rows[0]["date"] == "2024-01-01"
    assert rows[0]["precip_mm"] == "10.0"
    assert rows[0]["et_mm"] == "2.0"
    assert rows[0]["tracer_upstream_mgL"] == "5.0"
    assert rows[1]["date"] == "2024-01-02"
    assert rows[1]["precip_mm"] == "0.0"
    assert rows[1]["et_mm"] == "3.0"
    assert rows[1]["tracer_upstream_mgL"] == "4.5"
