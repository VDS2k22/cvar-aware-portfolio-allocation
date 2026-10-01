import numpy as np
import pandas as pd
from src.data_pipeline import transform_prices


def test_forward_return_definition():
    idx = pd.bdate_range("2020-01-01", periods=10)
    tickers = ["SPY", "EFA", "EEM", "IEF", "TLT", "LQD", "GLD", "DBC"]

    prices = pd.DataFrame(
        {ticker: np.arange(100, 110, dtype=float) for ticker in tickers},
        index=idx,
    )

    out = transform_prices(prices)
    expected = prices.iloc[5, 0] / prices.iloc[0, 0] - 1
    actual = out["forward_5d_returns"].iloc[0, 0]

    assert np.isclose(actual, expected)
