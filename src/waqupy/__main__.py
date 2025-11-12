"""Command-line interface module for waqupy water quality model."""

import argparse
from pathlib import Path

from waqupy.data_types import ForcingRow, ReachRow, read_table_from_csv
from waqupy.water_model import run_all


# AI-ASSIST: AI wrote the argument parser.
def main() -> None:
    """Command-line interface function for waqupy."""
    parser = argparse.ArgumentParser(description="Waqupy water quality model")
    parser.add_argument("--forcing", type=Path, help="Path to forcing CSV file")
    parser.add_argument("--reaches", type=Path, help="Path to reaches CSV file")
    parser.add_argument("--out", type=Path, help="Path to output CSV file")

    args = parser.parse_args()

    forcing = read_table_from_csv(args.forcing, ForcingRow)
    reaches = read_table_from_csv(args.reaches, ReachRow)
    discharge = run_all(forcing, reaches)
    discharge.to_csv(args.out)


if __name__ == "__main__":
    main()
