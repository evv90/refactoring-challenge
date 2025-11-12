# ruff: noqa: PLR2004 - allow "magic numbers" in tests
"""Tests for waqupy.utils module."""

import textwrap
from typing import TYPE_CHECKING

import pytest

from waqupy.data_types import Forcing, parse_date, read_table_from_csv

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
def test_read_forcing_csv(tmp_path: Path) -> None:
    """Test the read_csv_as_dicts function with a sample CSV file."""
    csv_content = textwrap.dedent(
        """\
        date,precip_mm,et_mm,tracer_upstream_mgL
        2024-01-01, 10.0, 2.0, 5.0
        2024-01-02, 0.0, 3.0, 4.5
        """
    )
    csv_path = tmp_path / "forcing.csv"
    csv_path.write_text(csv_content, encoding="utf-8")
    forcing = read_table_from_csv(csv_path, Forcing)
    assert len(forcing.rows) == 2
    row1 = forcing.rows[0]
    assert row1.date.year == 2024
    assert row1.date.month == 1
    assert row1.date.day == 1
    assert row1.precip_mm == 10.0
    assert row1.et_mm == 2.0
    assert row1.tracer_upstream_mgL == 5.0
    row2 = forcing.rows[1]
    assert row2.date.year == 2024
    assert row2.date.month == 1
    assert row2.date.day == 2
    assert row2.precip_mm == 0.0
    assert row2.et_mm == 3.0
    assert row2.tracer_upstream_mgL == 4.5
