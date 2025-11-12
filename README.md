# Documentation for waqupy

See also [github.com/evv90/refactoring-challenge](https://github.com/evv90/refactoring-challenge)

A package for calculating a daily water balance and a conservative tracer concentration across two linked river reaches.

## Installation

```
poetry install --with dev
```

## Usage

Use the CLI:

```
python -m waqupy --forcing tests/input_data/forcing.csv --reaches tests/input_data/reaches.csv --out results.csv
```

Run the tests:

```
pytest
```

## Methods

The two reaches A and B are updated for each timestep:

The tracer concentrations are updated using

$$
C_A(t_{n+1}) = M(1, C_U(t_{n+1}), D(t_{n+1}), C_A(t_{n}))
$$ 

$$
C_B(t_{n+1}) = M(D_A(t_{n+1}), C_A(t_{n+1}), D(t_{n+1}), C_A(t_{n}))
$$ 

where $C_x(t)$ is the tracer concentration for reach $x$ at timestep $t$, and $D_x(t)$ is its discharge. $C_U(t)$ is the upstream tracer concentration. $M$ is the weighed mixing formula.

$$
M(q_a, c_a, q_b, c_b) = (q_a \cdot c_a + q_b \cdot c_b) / (q_a + q_b).
$$

The upstream tracer concentration is given input.

The discharge is calculated by simple bucket runoff in the reach area.
