# Intentionally fragile utilities with duplicated logic and inconsistent styles.
# HINT: In refactor, consolidate CSV parsing and use standard libraries robustly.

from __future__ import annotations

import csv
from datetime import date
from typing import Any, Dict, List

# Global mutable cache — smell
CACHE: Dict[str, Any] = {}


def parse_date(text: str) -> date:
    """Date parser. Supports YYYY-MM-DD and YYYY/MM/DD."""
    return date.fromisoformat(text.replace("/", "-"))


def read_csv_as_dicts(path: str) -> List[Dict[str, str]]:
    # Duplicated logic with read_csv_to_rows
    rows: List[Dict[str, str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k.strip(): v.strip() for k, v in r.items()})
    return rows


def read_csv_to_rows(path: str) -> List[List[str]]:
    # Duplicated logic with read_csv_as_dicts
    out: List[List[str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            out.append([x.strip() for x in r])
    return out
