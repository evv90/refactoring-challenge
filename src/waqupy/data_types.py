"""Data classes and table handling for Waqupy."""

import csv
from dataclasses import asdict, dataclass, fields
from datetime import date
from typing import TYPE_CHECKING, Protocol, Self, TypeVar

if TYPE_CHECKING:
    from pathlib import Path

# AI-ASSIST: AI wrote all the from_str_dict methods

# Note: all this work would be unnecessary if I could use
# pydantic or pandas, or something like that.


def parse_date(text: str) -> date:
    """Date parser. Supports YYYY-MM-DD and YYYY/MM/DD."""
    return date.fromisoformat(text.replace("/", "-"))


@dataclass
class TableRow(Protocol):
    """Protocol for a row in a generic table."""

    @classmethod
    def from_str_dict(cls, data: dict[str, str]) -> Self:
        """Create a TableRow from a dictionary of strings."""
        ...


def field_names(table_row: TableRow) -> list[str]:
    """Get all TableRow field names."""
    return [f.name for f in fields(table_row)]


@dataclass
class Forcing(TableRow):
    """Data class for a row in a discharge table."""

    date: date
    precip_mm: float
    et_mm: float
    tracer_upstream_mgL: float  # noqa: N815 - allow upper case for litre unit

    @classmethod
    def from_str_dict(cls, data: dict[str, str]) -> Self:
        """Create a Forcing row from a dictionary of strings."""
        return cls(
            date=parse_date(data["date"]),
            precip_mm=float(data["precip_mm"]),
            et_mm=float(data["et_mm"]),
            tracer_upstream_mgL=float(data["tracer_upstream_mgL"]),
        )


@dataclass
class Reaches(TableRow):
    """Data class for a row in a reaches table."""

    reach_id: str
    area_km2: float
    tracer_init_mgL: float  # noqa: N815 - allow upper case for litre unit

    @classmethod
    def from_str_dict(cls, data: dict[str, str]) -> Self:
        """Create a Reaches row from a dictionary of strings."""
        return cls(
            reach_id=data["reach_id"],
            area_km2=float(data["area_km2"]),
            tracer_init_mgL=float(data["tracer_init_mgL"]),
        )


@dataclass
class Discharge(TableRow):
    """Data class for a row in a discharge table."""

    date: date
    reach: str
    q_m3s: float
    c_mgL: float  # noqa: N815 - allow upper case for litre unit

    @classmethod
    def from_str_dict(cls, data: dict[str, str]) -> Self:
        """Create a Discharge row from a dictionary of strings."""
        return cls(
            date=parse_date(data["date"]),
            reach=data["reach"],
            q_m3s=float(data["q_m3s"]),
            c_mgL=float(data["c_mgL"]),
        )


T = TypeVar("T", bound=TableRow)


class Table[T: TableRow]:
    """Class to handle waqupy data tables."""

    def __init__(self) -> None:
        """Initialize an empty Table."""
        self._rows: list[T] = []

    @property
    def rows(self) -> list[T]:
        """Get all rows in the Table."""
        return self._rows

    def add_row(self, row: T) -> None:
        """Add a row to the Table."""
        self._rows.append(row)

    def to_csv(self, path: Path) -> None:
        """Write the Table to a CSV file."""
        if len(self._rows) == 0:
            msg = "Cannot write empty table to CSV"
            raise RuntimeError(msg)
        fields = field_names(self._rows[0])
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fields)
            w.writeheader()
            for r in self._rows:
                w.writerow(asdict(r))


def read_table_from_csv(path: Path, table_type: type[TableRow]) -> Table:
    """Create a Table from a CSV file."""
    table = Table[table_type]()  # type: ignore[valid-type]
    with path.open("r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row_dict in r:
            row = table_type.from_str_dict(row_dict)
            table.add_row(row)
    return table
