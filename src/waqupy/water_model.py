"""Main run loop for wqaupy water quality model."""

from waqupy.data_types import Discharge, Forcing, Reaches, Table


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


def run_step(
    forcing: Forcing,
    reaches_a: Reaches,
    reaches_b: Reaches,
    concentration_a: float,
    concentration_b: float,
) -> tuple[Discharge, Discharge]:
    """Run a single time step of the water quality model."""
    upstream_c = forcing.tracer_upstream_mgL

    runoff_mm = max(forcing.precip_mm - forcing.et_mm, 0.0)

    discharge_a = mm_day_to_m3s(runoff_mm, reaches_a.area_km2)
    discharge_b = mm_day_to_m3s(runoff_mm, reaches_b.area_km2)

    mixed_concentration_a = mix_concentration(
        q1=1.0, c1=upstream_c, q2=discharge_a, c2=concentration_a
    )

    result_a = Discharge(
        date=forcing.date,
        reach=reaches_a.reach_id,
        q_m3s=discharge_a,
        c_mgL=mixed_concentration_a,
    )

    mixed_concentration_b = mix_concentration(
        q1=discharge_a,
        c1=mixed_concentration_a,
        q2=discharge_b,
        c2=concentration_b,
    )

    discharge_total = discharge_a + discharge_b
    result_b = Discharge(
        date=forcing.date,
        reach=reaches_b.reach_id,
        q_m3s=discharge_total,
        c_mgL=mixed_concentration_b,
    )
    return result_a, result_b


def run_all(forcing: Table[Forcing], reaches: Table[Reaches]) -> Table[Discharge]:
    """Run the water quality model for all reaches."""
    if len(reaches.rows) != 2:
        msg = "This model needs exactly 2 reaches as input."
        raise RuntimeError(msg)

    reaches_a = reaches.rows[0]
    reaches_b = reaches.rows[1]

    concentration_a = reaches_a.tracer_init_mgL
    concentration_b = reaches_b.tracer_init_mgL

    results = Table[Discharge]()

    for f in forcing.rows:
        discharge_a, discharge_b = run_step(
            f,
            reaches_a,
            reaches_b,
            concentration_a,
            concentration_b,
        )
        concentration_a = discharge_a.c_mgL
        concentration_b = discharge_b.c_mgL
        results.add_row(discharge_a)
        results.add_row(discharge_b)

    return results
