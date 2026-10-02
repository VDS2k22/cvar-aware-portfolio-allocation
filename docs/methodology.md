# Baseline Methodology

## Data universe
Daily adjusted price data for eight liquid ETFs:

- SPY — US equities
- EFA — Developed ex-US equities
- EEM — Emerging-market equities
- IEF — Intermediate US Treasuries
- TLT — Long-term US Treasuries
- LQD — Investment-grade corporate bonds
- GLD — Gold
- DBC — Broad commodities

## Sample
2010-01-01 through 2025-12-31.

## Core transformations
The baseline pipeline creates:

- aligned adjusted close prices
- daily simple returns
- daily log returns
- next-5-trading-day forward returns
- weekly prices
- weekly returns
- data-quality diagnostics

## Modelling split
- Train: 2010–2016
- Validation: 2017–2018
- Test: 2019–2025

## Leakage control
Because the supervised target is the next five trading days, the modelling workflow uses a five-trading-day purge at chronological sample boundaries.

## Benchmark portfolios
The initial notebook implements:
- Equal Weight
- Mean-Variance
- Risk Parity

The ML forecasting and CVaR optimisation layers are intentionally outside this baseline commit.
