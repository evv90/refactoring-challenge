"""Tests for checking if code behavior is the same as legacy code."""

import filecmp
from pathlib import Path

from waqupy.__main__ import write_output_csv
from waqupy.utils import read_csv_as_dicts
from waqupy.water_model import run_all

TEST_DIR_PATH = Path(__file__).parent


def test_legacy_data(tmp_path: Path) -> None:
    """Test if running on originally provided data returns expected results."""

    forcing_list = read_csv_as_dicts(TEST_DIR_PATH / "input_data" / "forcing.csv")
    reaches_list = read_csv_as_dicts(TEST_DIR_PATH / "input_data" / "reaches.csv")
    rows = run_all(forcing_list, reaches_list)
    write_output_csv(tmp_path / "legacy_results.csv", rows)

    # TODO: for now we test the resulting files against each other.
    # After refactoring, we should just check the result objects directly.
    ref_path = TEST_DIR_PATH / "references" / "legacy_results.csv"
    assert filecmp.cmp(tmp_path / "legacy_results.csv", ref_path)
