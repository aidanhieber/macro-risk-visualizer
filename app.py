# --- app.py ---
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from utils import preprocess_data

st.title("Credit Spreads, Consumer Sentiment & Market Selloffs")
st.write("""
    This tool visualizes investment-grade credit spreads and consumer sentiment,
    overlaying periods of significant market drawdowns for the selected dates.
""")

df = preprocess_data()

# Debug output
st.write("### Debug: Full Data Overview")
st.dataframe(df.head(10))

start_date = st.date_input("Start Date", value=datetime(2004, 1, 1), min_value=datetime(2003, 1, 1))
end_date = st.date_input("End Date", value=datetime.today())

df_filtered = df[(df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))]

if not df_filtered.empty:
    st.line_chart(df_filtered[["Credit Spread", "Sentiment"]])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_filtered.index, df_filtered["S&P 500"], label="S&P 500", color="black")
    ax.fill_between(df_filtered.index, df_filtered["S&P 500"], where=df_filtered["Selloff"],
                    color="red", alpha=0.3, label="Selloff")
    ax.set_title("S&P 500 with Selloff Periods")
    ax.legend()
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    fig.autofmt_xdate()
    st.pyplot(fig)

    st.write("Preview of merged data")
    st.dataframe(df_filtered.tail(10))
else:
    st.warning("No data available in the selected date range. Please adjust the dates.")
