import pandas as pd

def add_predictive_signal(
    df,
    spread_col="Credit Spread",
    sentiment_col="Sentiment",
    spread_threshold=0.10,
    sentiment_drop_threshold=-0.10,
    sentiment_level=70
):
    """
    Adds a predictive signal column based on:
    - Increase in credit spreads (10% or more over previous month)
    - Drop in consumer sentiment (10%+ decline from previous month)
      OR sentiment below a pessimistic threshold (e.g., 70)
    """
    df = df.copy()
    df["Spread Change"] = df[spread_col].pct_change()
    df["Sentiment Change"] = df[sentiment_col].pct_change()

    sentiment_condition = (
        (df["Sentiment Change"] < sentiment_drop_threshold) |
        (df[sentiment_col] < sentiment_level)
    )

    df["Signal"] = (df["Spread Change"] > spread_threshold) & sentiment_condition
    return df

