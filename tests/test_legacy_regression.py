"""Tests for checking if code behavior is the same as legacy code."""
import filecmp
from pathlib import Path

from waqupy import water_model
from waqupy.config import Config

TEST_DIR_PATH = Path(__file__).parent


def test_legacy_data(tmp_path: Path) -> None:
    """Test if running on originally provided data returns expected results."""
    config = Config(
        forcing_path=TEST_DIR_PATH / "input_data" / "forcing.csv",
        reaches_path=TEST_DIR_PATH / "input_data" / "reaches.csv",
        output_path=tmp_path / "legacy_results.csv"
    )
    water_model.main(config)

    # TODO: for now we test the resulting files against each other.
    # After refactoring, we should just check the result objects directly.
    ref_path = TEST_DIR_PATH / "references" / "legacy_results.csv"
    assert filecmp.cmp(tmp_path / "legacy_results.csv", ref_path)
