# cvar-aware-portfolio-allocation
Research code for dynamic multi-asset portfolio allocation using machine-learning forecasts and CVaR-based tail-risk constraints
## Initial implementation

`MScFE_690_XGBoost.ipynb` contains the current modelling pipeline, including:

- ETF data download and validation
- feature construction
- five-day forward-return targets
- XGBoost forecasting
- benchmark portfolio construction
- walk-forward out-of-sample evaluation
- preliminary performance results

## Repository structure

- `src/` – data preparation, portfolio construction and backtesting modules
- `notebooks/` – baseline analysis and exploratory notebooks
- `tests/` – validation tests for the implementation
- `data/` – project data structure
- `outputs/` – generated results and analysis outputs
- `MScFE_690_XGBoost.ipynb` – initial XGBoost forecasting and portfolio modelling notebook

The baseline implementation covers data acquisition and validation, return construction,
train/validation/test preparation, leakage controls, benchmark portfolios and walk-forward
backtesting. The XGBoost notebook extends this work with an initial machine-learning
forecasting framework.

### Running the notebook

The notebook can be opened and run in Google Colab or Jupyter Notebook.

Install the required packages using:

pip install -r requirements.txt

The current implementation is preliminary. CVaR optimisation, transaction costs and further model development are work in progress.
