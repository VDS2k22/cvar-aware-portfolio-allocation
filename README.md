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

### Running the notebook

The notebook can be opened and run in Google Colab or Jupyter Notebook.

Install the required packages using:

pip install -r requirements.txt

The current implementation is preliminary. CVaR optimisation, transaction costs and further model development are work in progress.
