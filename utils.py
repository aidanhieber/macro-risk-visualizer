import pandas as pd
import numpy as np
from data_loader import load_fred_data
from config import CREDIT_SPREAD_TICKER, SENTIMENT_TICKER, SP500_TICKER

def calculate_drawdowns(price_series):
    roll_max = price_series.cummax()
    drawdown = (price_series - roll_max) / roll_max
    return drawdown

def preprocess_data(start_date="2004-01-01", method="last"):
    spread = load_fred_data(CREDIT_SPREAD_TICKER, start_date)
    sentiment = load_fred_data(SENTIMENT_TICKER, start_date)
    spx = load_fred_data(SP500_TICKER, start_date)

    if spread is None or sentiment is None or spx is None:
        print("ERROR - One or more datasets failed to load.")
        return None

    spread_monthly = spread.resample("MS").last()
    sentiment_monthly = sentiment.resample("MS").last()
    spread_monthly.columns = ["Credit Spread"]
    sentiment_monthly.columns = ["Sentiment"]

    spx_monthly_last = spx.resample("MS").last()
    spx_monthly_min = spx.resample("MS").min()

    # Use last for returns
    spx_returns = spx_monthly_last.pct_change() * 100
    spx_returns = spx_returns.reindex(spx_monthly_last.index)
    spx_returns.columns = ["S&P 500 Returns"]

    # Use min for drawdowns
    drawdown_source = spx_monthly_min
    drawdown = calculate_drawdowns(drawdown_source)
    drawdown_df = pd.DataFrame(drawdown)
    drawdown_df.columns = ["Drawdown"]

    selloff = (drawdown <= -0.10).astype(bool)
    selloff_df = pd.DataFrame(selloff)
    selloff_df.columns = ["Selloff"]

    spx_monthly_last.rename(columns={spx_monthly_last.columns[0]: "S&P 500"}, inplace=True)

    df = pd.concat([
        spread_monthly,
        sentiment_monthly,
        spx_monthly_last,
        spx_returns,
        drawdown_df,
        selloff_df
    ], axis=1)

    df.dropna(inplace=True)

    df.attrs["sp500_trace"] = {
        "name": "S&P 500",
        "showlegend": False,
        "line": dict(color="#333")
    }

    return df
