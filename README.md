# CVaR-Aware Multi-Asset Portfolio Allocation

Research code for the MScFE 690 Capstone Project:

**Machine Learning-Driven Dynamic Portfolio Optimization Under Tail-Risk Constraints: A CVaR-Aware Framework for Multi-Asset Allocation**

## Research question

Does applying a 95% Conditional Value-at-Risk (CVaR) constraint to a weekly multi-asset ETF portfolio driven by machine-learning return forecasts reduce realised tail risk and improve risk-adjusted performance after transaction costs?

## Investment universe

The analysis uses eight liquid ETFs:

- SPY — US equities
- EFA — Developed-market equities outside North America
- EEM — Emerging-market equities
- IEF — Intermediate US Treasuries
- TLT — Long-term US Treasuries
- LQD — Investment-grade corporate bonds
- GLD — Gold
- DBC — Broad commodities

Daily market data cover 2010–2025.

## Experimental design

The final experiment compares four weekly portfolios:

| Portfolio | Return forecast | CVaR constraint |
|---|---|---|
| XGBoost Base | XGBoost | No |
| XGBoost-CVaR | XGBoost | Yes |
| NoForecast Base | Zero expected returns | No |
| NoForecast-CVaR | Zero expected returns | Yes |

The main comparison is between **XGBoost Base** and **XGBoost-CVaR**. The forecasting model, covariance estimates, portfolio constraints, risk-aversion parameter, turnover penalty, rebalancing frequency and transaction-cost assumptions are held comparable so that the incremental effect of the CVaR constraint can be examined.

## Methodology

The workflow includes:

- chronological train, validation and test periods
- five-trading-day forecast target
- five-day purge to reduce leakage
- separate XGBoost models for each ETF
- expanding-window weekly forecasting
- trailing 252-day covariance estimation
- long-only portfolio optimisation with a 30% maximum asset weight
- 95% historical CVaR constraint
- turnover penalty
- transaction costs
- no-forecast control portfolios
- stress-period and feasible-week analysis
- paired block-bootstrap confidence intervals

The main out-of-sample test period is 2019–2025 and contains 365 weekly portfolio decisions.

## Main notebook

`notebooks/MScFE_690_CVaR_Transaction_Costs.ipynb`

contains the final XGBoost/CVaR portfolio experiment.

## Reported results

In the M6 analysis at 10 bps transaction costs:

| Portfolio | Annualised return | Volatility | Sharpe | Realised CVaR 95% |
|---|---:|---:|---:|---:|
| XGBoost Base | 8.42% | 9.41% | 0.633 | 2.85% |
| XGBoost-CVaR | 9.07% | 8.96% | 0.727 | 2.63% |
| NoForecast Base | 5.99% | 8.63% | 0.419 | 2.61% |
| NoForecast-CVaR | 6.08% | 8.48% | 0.435 | 2.55% |

The CVaR constraint was feasible in 262 of 365 test weeks. In the remaining 103 weeks, the unconstrained allocation was used as the operational fallback.

Bootstrap confidence intervals for the main performance differences include zero, so the observed improvements should not be interpreted as statistically conclusive.

## Reproducibility note

Market data are obtained from Yahoo Finance. Historical adjusted prices may be revised by the data provider over time. As a result, rerunning the notebook with a later Yahoo Finance data vintage may produce small numerical differences even when the model configuration and random seeds are unchanged.

The methodology and qualitative conclusions should therefore be distinguished from exact results associated with a particular data download.

## Repository structure

- `notebooks/` — baseline and final analysis notebooks
- `src/` — reusable data-preparation code
- `tests/` — implementation checks
- `data/` — data directory structure
- `outputs/` — generated analysis outputs
- `docs/` — methodology documentation
- `requirements.txt` — Python dependencies

## Running the analysis

Install the required packages:

```bash
pip install -r requirements.txt
```

Then open the notebooks using Jupyter Notebook, JupyterLab or Google Colab.

The project uses Python with pandas, NumPy, XGBoost, CVXPY, SciPy, scikit-learn, Matplotlib and yfinance.
