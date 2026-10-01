from pathlib import Path
import numpy as np
import pandas as pd
import yfinance as yf

TICKERS = ["SPY", "EFA", "EEM", "IEF", "TLT", "LQD", "GLD", "DBC"]
START_DATE = "2010-01-01"
END_DATE = "2026-01-01"  # Yahoo end date is exclusive


def download_prices(tickers=TICKERS, start=START_DATE, end=END_DATE):
    """Download daily Yahoo Finance data and return raw data + adjusted close prices."""
    raw = yf.download(
        tickers,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        group_by="column",
        progress=False,
        threads=True,
    )

    if not isinstance(raw.columns, pd.MultiIndex):
        raise ValueError("Unexpected Yahoo Finance output structure.")
    if "Adj Close" not in raw.columns.get_level_values(0):
        raise KeyError("Adjusted Close field was not returned.")

    prices = raw["Adj Close"].reindex(columns=tickers).sort_index()
    prices.index = pd.to_datetime(prices.index)
    return raw, prices


def validate_prices(prices: pd.DataFrame) -> pd.DataFrame:
    diagnostic_returns = prices.pct_change(fill_method=None)
    rows = []

    for ticker in prices.columns:
        s = prices[ticker]
        rows.append({
            "Ticker": ticker,
            "First_Valid_Date": s.first_valid_index(),
            "Last_Valid_Date": s.last_valid_index(),
            "Observations": int(s.notna().sum()),
            "Missing_Values": int(s.isna().sum()),
            "Non_Positive_Prices": int((s.dropna() <= 0).sum()),
            "Min_Daily_Return": diagnostic_returns[ticker].min(),
            "Max_Daily_Return": diagnostic_returns[ticker].max(),
            "Abs_Return_Above_20pct": int((diagnostic_returns[ticker].abs() > 0.20).sum()),
        })

    report = pd.DataFrame(rows)
    report["Duplicate_Dates_In_Index"] = int(prices.index.duplicated().sum())
    return report


def transform_prices(prices: pd.DataFrame):
    """Align prices and derive baseline return datasets."""
    aligned = prices.dropna(how="any").copy()
    daily_returns = aligned.pct_change(fill_method=None).dropna()
    log_returns = np.log(aligned / aligned.shift(1)).dropna()
    forward_5d_returns = aligned.shift(-5) / aligned - 1
    weekly_prices = aligned.resample("W-FRI").last().dropna()
    weekly_returns = weekly_prices.pct_change(fill_method=None).dropna()

    return {
        "adjusted_close": aligned,
        "daily_returns": daily_returns,
        "log_returns": log_returns,
        "forward_5d_returns": forward_5d_returns,
        "weekly_prices": weekly_prices,
        "weekly_returns": weekly_returns,
    }


def save_pipeline_outputs(base_dir="."):
    base = Path(base_dir)
    for p in [
        base / "data" / "raw",
        base / "data" / "processed",
        base / "data" / "validation",
    ]:
        p.mkdir(parents=True, exist_ok=True)

    raw, prices = download_prices()
    raw.to_csv(base / "data" / "raw" / "yahoo_etf_raw.csv")

    report = validate_prices(prices)
    report.to_csv(base / "data" / "validation" / "data_quality_report.csv", index=False)

    outputs = transform_prices(prices)
    for name, df in outputs.items():
        df.to_csv(base / "data" / "processed" / f"{name}.csv")

    return outputs, report


if __name__ == "__main__":
    outputs, report = save_pipeline_outputs(".")
    print(report)
    print("\nSaved processed datasets:")
    for name, df in outputs.items():
        print(f"{name}: {df.shape}")
