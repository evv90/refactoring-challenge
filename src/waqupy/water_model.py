"""Main run loop for wqaupy water quality model."""
from typing import Any

from waqupy.utils import parse_date


def mm_day_to_m3s(mm_per_day: float, area_km2: float) -> float:
    """Convert mm/day over area in km^2 to m^3/s."""
    if area_km2 == 0:
        return 0.0
    return (mm_per_day / 1000.0) * (area_km2 * 1.0e6) / 86400.0


def mix_concentration(q1: float, c1: float, q2: float, c2: float) -> float:
    """Flow-weighted mixing."""
    if q1 + q2 == 0:
        return float("nan")
    return (q1 * c1 + q2*c2) / (q1 + q2)


def run_all(forcing: list[dict[str, str]], reaches: list[dict[str, str]]):
    """Run the water quality model for all reaches."""
    if len(reaches) < 2:
        msg = "need at least 2 reaches A and B"
        raise RuntimeError(msg)

    # Assume reaches sorted A then B
    A = reaches[0]
    B = reaches[1]

    A_area = float(A.get("area_km2", "0"))
    B_area = float(B.get("area_km2", "0"))

    C_A = float(A.get("tracer_init_mgL", "0"))
    C_B = float(B.get("tracer_init_mgL", "0"))

    results: list[dict[str, Any]] = []

    for row in forcing:
        d = parse_date(row.get("date", "1970-01-01"))
        P = float(row.get("precip_mm", "0"))
        ET = float(row.get("et_mm", "0"))
        upstream_c = float(row.get("tracer_upstream_mgL", "0"))

        runoff_mm_A = max(P - ET, 0.0)
        runoff_mm_B = max(P - ET, 0.0)

        discharge_A = mm_day_to_m3s(runoff_mm_A, A_area)
        discharge_B = mm_day_to_m3s(runoff_mm_B, B_area)

        C_A = mix_concentration(q1=1.0, c1=upstream_c, q2=discharge_A, c2=C_A)

        results.append({
            "date": d.isoformat(), "reach": "A", "q_m3s": discharge_A, "c_mgL": C_A
        })

        C_B = mix_concentration(q1=discharge_A, c1=C_A, q2=discharge_B, c2=C_B)

        discharge_total = discharge_A + discharge_B
        results.append({
            "date": d.isoformat(), "reach": "B", "q_m3s": discharge_total, "c_mgL": C_B
        })

    return results
