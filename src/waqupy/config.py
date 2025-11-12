"""Configuration for Waqupy hydrological model."""
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class Config:
    """Configuration parameters for Waqupy model."""

    forcing_path: Path
    reaches_path: Path
    output_path: Path
    beta: float = 0.85
    tracer_units: str = "mg/L"
    catchment_area_units: str = "km2"
