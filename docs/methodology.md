# Final Methodology

## Data universe

The analysis uses daily adjusted price and volume data from Yahoo Finance for eight ETFs:

- SPY — US equities
- EFA — Developed-market equities outside North America
- EEM — Emerging-market equities
- IEF — Intermediate US Treasuries
- TLT — Long-term US Treasuries
- LQD — Investment-grade corporate bonds
- GLD — Gold
- DBC — Broad commodities

The sample covers 2010–2025.

## Sample design

The modelling periods are chronological:

- Train: 2010–2016
- Validation: 2017–2018
- Test: 2019–2025

A five-trading-day purge is applied at sample boundaries because the supervised target is the forward five-day return.

## XGBoost forecasting

A separate XGBoost regression model is estimated for each ETF to forecast five-trading-day returns.

The same configuration is used across assets and weekly refits:

- Objective: squared error
- Trees: 300
- Maximum depth: 3
- Learning rate: 0.03
- Row subsample: 0.80
- Column subsample: 0.80
- Minimum child weight: 5
- L1 penalty: 0.10
- L2 penalty: 1.00
- Random seed: 42

Forecast accuracy is evaluated using RMSE, MAE and the correlation between predicted and realised five-day returns.

## Portfolio optimisation

At each weekly decision date, portfolio risk is estimated using the preceding 252 trading days of daily returns. The daily covariance matrix is scaled to the five-day forecast horizon.

Portfolio weights maximise predicted return while penalising portfolio variance and turnover.

The constraints are:

- fully invested portfolio
- long-only weights
- maximum 30% weight in any ETF

The optimisation uses:

- risk-aversion parameter: λ = 20
- turnover penalty: γ = 0.005

These parameters were selected using the 2017–2018 validation period and then held fixed throughout the test period.

## Experimental design

Four portfolios are evaluated:

| Portfolio | Expected returns | CVaR constraint |
|---|---|---|
| XGBoost Base | XGBoost forecasts | No |
| XGBoost-CVaR | XGBoost forecasts | Yes |
| NoForecast Base | Zero | No |
| NoForecast-CVaR | Zero | Yes |

The NoForecast portfolios retain the same covariance estimates, portfolio constraints, risk-aversion parameter and turnover penalty. This provides a control for assessing the effect of the XGBoost forecasts.

## CVaR constraint

The CVaR portfolios use a 95% historical CVaR constraint based on overlapping five-day joint return scenarios constructed from the preceding 252 trading days.

The CVaR limit is:

`0.025377`

or approximately 2.54%.

The limit was calibrated using information available before 1 January 2019, so test-period observations were not used in its selection.

## Feasibility and fallback

If the CVaR-constrained optimisation does not return an accepted solution, the corresponding unconstrained portfolio allocation is used as the operational fallback.

Across the 365 out-of-sample test weeks:

- 262 weeks are CVaR-feasible
- 103 weeks use the unconstrained fallback

The full-period CVaR strategy should therefore be interpreted as a constrained strategy with an unconstrained fallback rather than continuous enforcement of the CVaR limit.

## Transaction costs

Net portfolio returns deduct proportional transaction costs based on portfolio turnover.

The main analysis assumes:

- 10 basis points per unit of turnover

Sensitivity tests also use:

- 5 basis points
- 20 basis points

The same transaction-cost assumptions are applied to all four portfolios.

## Rebalancing and execution

The final available trading day in each Friday-ending week is used as the feature and rebalance reference date.

Portfolio weights are applied to returns from that close to the following weekly close.

The backtest includes proportional transaction costs but does not explicitly model next-open execution, intraday slippage, market impact or time-varying liquidity costs.

## Evaluation

Portfolio performance is evaluated using:

- annualised return
- annualised volatility
- Sharpe ratio
- Sortino ratio
- maximum drawdown
- realised 95% and 99% CVaR
- portfolio turnover
- transaction costs
- portfolio concentration and weight diagnostics

## Statistical inference

A paired block bootstrap is used to assess uncertainty in the differences between strategies.

The procedure uses:

- four-week return blocks
- identical blocks for each paired strategy
- 2,000 bootstrap replications
- 95% percentile confidence intervals

The bootstrap evaluates differences in annualised return, Sharpe ratio, realised 95% CVaR and maximum drawdown.
