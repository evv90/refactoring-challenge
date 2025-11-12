"""Tests for legacy bugs in waqupy.water_model module."""

import math

from waqupy import water_model


def test_tracer_mixing_should_be_flow_weighted() -> None:
    """Test if flow-weighted mixing returns expected value."""
    q1, c1 = 1.0, 10.0
    q2, c2 = 3.0, 0.0
    expected = (q1 * c1 + q2 * c2) / (q1 + q2)  # 2.5 mg/L

    got = water_model.mix_concentration(q1, c1, q2, c2)

    assert math.isclose(got, expected, rel_tol=1e-9), (
        "Legacy tracer mixing is incorrect; should be flow-weighted mass balance"
    )


def test_mm_day_to_m3s_conversion() -> None:
    """Test precipitation conversion: 86.4 mm/day over 1 km^2 should yield 1 m^3/s."""
    mm_per_day = 86.4
    area_km2 = 1.0
    expected = 1.0

    got = water_model.mm_day_to_m3s(mm_per_day, area_km2)

    assert math.isclose(got, expected, rel_tol=1e-12), (
        "Legacy unit conversion mm/day -> m^3/s is incorrect"
    )
