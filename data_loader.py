import pandas as pd
from fredapi import Fred
from config import FRED_API_KEY, CREDIT_SPREAD_TICKER, SENTIMENT_TICKER, SP500_TICKER

fred = Fred(api_key=FRED_API_KEY)

def load_fred_data(ticker, start_date):
    start = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    print(f"Fetching {ticker} from FRED starting {start}")
    data = fred.get_series(ticker, start_date=start)
    if data is None or data.empty:
        print(f"⚠️ WARNING: No data returned for {ticker}")
        return pd.DataFrame(columns=[ticker])
    return data.to_frame(name=ticker)