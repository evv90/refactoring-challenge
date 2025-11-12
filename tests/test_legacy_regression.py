"""Tests for checking if code behavior is the same as legacy code."""

import math
from pathlib import Path

from waqupy.data_types import ForcingRow, ReachRow, ResultRow, read_table_from_csv
from waqupy.water_model import run_all

TEST_DIR_PATH = Path(__file__).parent


def test_legacy_data() -> None:
    """Test if running on originally provided data returns expected results."""
    forcing = read_table_from_csv(
        TEST_DIR_PATH / "input_data" / "forcing.csv", ForcingRow
    )
    reaches = read_table_from_csv(
        TEST_DIR_PATH / "input_data" / "reaches.csv", ReachRow
    )
    result = run_all(forcing, reaches)

    ref_path = TEST_DIR_PATH / "references" / "legacy_results.csv"
    ref = read_table_from_csv(ref_path, ResultRow)

    assert len(result.rows) == len(ref.rows)
    for r1, r2 in zip(result.rows, ref.rows, strict=True):
        if math.isnan(r2.c_mgL):
            assert math.isnan(r1.c_mgL)
        else:
            assert r1 == r2
