# signal_generator.py
import pandas as pd


def add_predictive_signal(df, spread_col="Credit Spread", sentiment_col="Sentiment",
                          spread_threshold=0.10, sentiment_threshold=70):
    """
    Adds a predictive signal column based on:
    - Increase in credit spreads (10% or more over previous month)
    - Consumer sentiment below 70
    """
    df = df.copy()
    df["Spread Change"] = df[spread_col].pct_change()
    df["Signal"] = (df["Spread Change"] > spread_threshold) & (df[sentiment_col] < sentiment_threshold)
    return df

