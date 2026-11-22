# CVaR-Aware Multi-Asset Portfolio Allocation

Research code for the MScFE 690 Capstone Project:

**Machine Learning-Driven Dynamic Portfolio Optimization Under Tail-Risk Constraints: A CVaR-Aware Framework for Multi-Asset Allocation**

## Start here

- **Main analysis (M7).** The current XGBoost and CVaR experiment, including transaction costs and the additional checks on allocations, market exposure, forecast rankings and drawdowns. [Open the M7 notebook](notebooks/MScFE_690_CVaR_Transaction_Costs.ipynb)
- **XGBoost methods companion.** The forecasting rationale, forecast diagnostics and comparisons with Equal Weight, Minimum Variance and inverse-volatility benchmarks. [Open the XGBoost notebook](notebooks/MScFE_690_XGBoost.ipynb)

### Archive

- **M6 milestone.** The earlier CVaR experiment and its saved results. [Open the M6 notebook](notebooks/archive/MScFE_690_CVaR_Transaction_Costs_M6.ipynb)
- **Data pipeline and initial benchmarks.** The initial data preparation, validation and benchmark backtest. [Open the data pipeline notebook](notebooks/archive/Data_Pipeline_Benchmarks.ipynb)

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

## Reported results

The saved M7 results below use a transaction cost of 10 bps.

| Portfolio | Annualised return | Volatility | Sharpe | Realised CVaR 95% |
|---|---:|---:|---:|---:|
| XGBoost Base | 8.51% | 9.43% | 0.640 | 2.85% |
| XGBoost-CVaR | 9.14% | 8.98% | 0.733 | 2.63% |
| NoForecast Base | 5.99% | 8.63% | 0.419 | 2.61% |
| NoForecast-CVaR | 6.08% | 8.48% | 0.435 | 2.55% |

The CVaR constraint was feasible in 262 of 365 test weeks. In the remaining 103 weeks, the unconstrained allocation was used as the operational fallback.

Compared with XGBoost Base, XGBoost-CVaR had lower realised 95% CVaR and a larger maximum drawdown (−18.15% versus −17.24%). The paired block-bootstrap confidence intervals for the main performance differences include zero.

## Reproducibility note

Market data are obtained from Yahoo Finance. Historical adjusted prices may be revised by the data provider over time. As a result, rerunning the notebook with a later Yahoo Finance data vintage may produce small numerical differences even when the model configuration and random seeds are unchanged.

The headline table uses the M7 data download. The archived M6 notebook retains the results from the earlier download.

## Repository structure

- `notebooks/` — current analysis and XGBoost methods companion
- `notebooks/archive/` — M6 milestone and initial data pipeline
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
