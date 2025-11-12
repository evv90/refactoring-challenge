"""Main run loop for wqaupy water quality model."""

from waqupy.data_types import ForcingRow, ReachRow, ResultRow, Table


def mm_day_to_m3s(mm_per_day: float, area_km2: float) -> float:
    """Convert mm/day over area in km^2 to m^3/s."""
    if area_km2 == 0:
        return 0.0
    return (mm_per_day / 1000.0) * (area_km2 * 1.0e6) / 86400.0


def mix_concentration(q1: float, c1: float, q2: float, c2: float) -> float:
    """Flow-weighted mixing."""
    if q1 + q2 == 0:
        return float("nan")
    return (q1 * c1 + q2 * c2) / (q1 + q2)


class Reach:
    """Class for storing Reach-specific information."""

    def __init__(self, reach_id: str, area: float, tracer_init: float) -> None:
        """Initialize Reach."""
        self.reach_id = reach_id
        self.area = area
        self.tracer_concentration = tracer_init
        self.discharge = 0.0

    def update(
        self, mixed_in_discharge: float, mixed_in_concentration: float, runoff: float
    ) -> None:
        """Use flow-weighted mixing to update concentration."""
        self.discharge = mm_day_to_m3s(runoff, self.area)
        self.tracer_concentration = mix_concentration(
            mixed_in_discharge,
            mixed_in_concentration,
            self.discharge,
            self.tracer_concentration,
        )


def run_all(forcing: Table[ForcingRow], reaches: Table[ReachRow]) -> Table[ResultRow]:
    """Run the water quality model for all reaches."""
    if len(reaches.rows) != 2:
        msg = "This model needs exactly 2 reaches as input."
        raise RuntimeError(msg)

    a = reaches.rows[0]
    b = reaches.rows[1]
    reach_a = Reach(a.reach_id, a.area_km2, a.tracer_init_mgL)
    reach_b = Reach(b.reach_id, b.area_km2, b.tracer_init_mgL)

    results = Table[ResultRow]()

    for f in forcing.rows:
        upstream_c = f.tracer_upstream_mgL
        runoff_mm = max(f.precip_mm - f.et_mm, 0.0)
        reach_a.update(
            mixed_in_discharge=1.0,
            mixed_in_concentration=upstream_c,
            runoff=runoff_mm,
        )
        reach_b.update(
            mixed_in_discharge=reach_a.discharge,
            mixed_in_concentration=reach_a.tracer_concentration,
            runoff=runoff_mm,
        )

        result_a = ResultRow(
            date=f.date,
            reach=reach_a.reach_id,
            q_m3s=reach_a.discharge,
            c_mgL=reach_a.tracer_concentration,
        )
        result_b = ResultRow(
            date=f.date,
            reach=reach_b.reach_id,
            q_m3s=reach_a.discharge + reach_b.discharge,
            c_mgL=reach_b.tracer_concentration,
        )
        results.add_row(result_a)
        results.add_row(result_b)

    return results
