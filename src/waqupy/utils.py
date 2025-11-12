"""Utility functions for Waqupy."""
import csv
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def parse_date(text: str) -> date:
    """Date parser. Supports YYYY-MM-DD and YYYY/MM/DD."""
    return date.fromisoformat(text.replace("/", "-"))


def read_csv_as_dicts(csv_path: Path) -> list[dict[str, str]]:
    """Read a CSV file and return a list of dictionaries."""
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [{k.strip(): v.strip() for k, v in r.items()} for r in reader]
