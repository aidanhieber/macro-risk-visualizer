import pandas as pd
import numpy as np
from data_loader import load_fred_data, load_sp500_data
from config import CREDIT_SPREAD_TICKER, SENTIMENT_TICKER

def calculate_drawdowns(price_series):
    roll_max = price_series.cummax()
    drawdown = (price_series - roll_max) / roll_max
    return drawdown

def preprocess_data(start_date="2004-01-01"):
    spread = load_fred_data(CREDIT_SPREAD_TICKER, start_date)
    sentiment = load_fred_data(SENTIMENT_TICKER, start_date)
    spx = load_sp500_data(start_date)

    print("DEBUG - Spread head:\n", spread.head())
    print("DEBUG - Sentiment head:\n", sentiment.head())
    print("DEBUG - SPX head:\n", spx.head())

    spread_monthly = spread.resample("M").last()
    sentiment_monthly = sentiment.resample("M").last()
    spx_monthly = spx.resample("M").last()

    df = pd.concat([spread_monthly, sentiment_monthly, spx_monthly], axis=1)
    df.columns = ["Credit Spread", "Sentiment", "S&P 500"]
    df.dropna(inplace=True)

    print("DEBUG - Combined DF head:\n", df.head())

    df["Drawdown"] = calculate_drawdowns(df["S&P 500"])
    df["Selloff"] = df["Drawdown"] <= -0.10

    return df
