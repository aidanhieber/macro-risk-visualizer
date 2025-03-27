import pandas as pd
import yfinance as yf
from fredapi import Fred
from config import FRED_API_KEY, CREDIT_SPREAD_TICKER, SENTIMENT_TICKER

fred = Fred(api_key=FRED_API_KEY)

def load_fred_data(ticker, start_date):
    data = fred.get_series(ticker)
    data = data[data.index >= pd.to_datetime(start_date)]
    return data.to_frame(name=ticker)

def load_sp500_data(start_date):
    spx = yf.download("^GSPC", start=start_date, progress=False, auto_adjust=False)
    if "Adj Close" in spx.columns:
        return spx["Adj Close"]
    elif "Close" in spx.columns:
        return spx["Close"]
    else:
        raise KeyError("Neither 'Adj Close' nor 'Close' found in S&P 500 data")
