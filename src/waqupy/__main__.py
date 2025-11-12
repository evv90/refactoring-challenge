"""Command-line interface for waqupy water quality model."""
import argparse
import csv
from pathlib import Path

from waqupy.utils import read_csv_as_dicts
from waqupy.water_model import run_all


def write_output_csv(path: str, rows) -> None:
    # TODO: to be refactored
    fieldnames = ["date", "reach", "q_m3s", "c_mgL"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


# AI-ASSIST: AI wrote the argument parser.
def main():
    parser = argparse.ArgumentParser(
        description="Waqupy water quality model"
    )
    parser.add_argument(
        "forcing",
        type=Path,
        help="Path to forcing CSV file"
    )
    parser.add_argument(
        "reaches",
        type=Path,
        help="Path to reaches CSV file"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("waqupy_output.csv"),
        help="Path to output CSV file"
    )

    args = parser.parse_args()

    forcing_list = read_csv_as_dicts(args.forcing)
    reaches_list = read_csv_as_dicts(args.reaches)
    rows = run_all(forcing_list, reaches_list)
    write_output_csv(args.output, rows)
    print(f"Wrote {len(rows)} rows to {args.output.to_posix()}")

if __name__ == "__main__":
    main()
