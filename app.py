import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from utils import preprocess_data
from signal_generator import add_predictive_signal

st.title("Credit Spreads, Consumer Sentiment & Market Selloffs")
st.write("""
    This tool visualizes investment-grade credit spreads and consumer sentiment,
    overlaying periods of significant market drawdowns for the selected dates.
""")

df = preprocess_data(method="last")
df = add_predictive_signal(df)

if df is None or df.empty or df.index.min() is pd.NaT or df.index.max() is pd.NaT:
    st.error("The dataset is empty or the index is invalid.")
else:
    earliest_date = df.index.min().date()
    latest_date = df.index.max().date()

    start_date = st.date_input("Start Date", value=earliest_date, min_value=earliest_date, max_value=latest_date)
    end_date = st.date_input("End Date", value=latest_date, min_value=earliest_date, max_value=latest_date)

    df_filtered = df[(df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))]

    show_sentiment = st.checkbox("Show Consumer Sentiment", value=True)
    show_spread = st.checkbox("Show Credit Spreads", value=True)
    show_returns = st.checkbox("Show S&P 500 Returns (Separate Chart)", value=True)
    show_signals = st.checkbox("Show Predictive Signals", value=True)

    if not df_filtered.empty:
        # --- PRIMARY MACRO-INDICATOR CHART ---
        fig_macro = go.Figure()

        if show_sentiment:
            fig_macro.add_trace(go.Scatter(
                x=df_filtered.index,
                y=df_filtered["Sentiment"],
                name="Sentiment",
                yaxis="y1",
                line=dict(color="green")
            ))

        if show_spread:
            fig_macro.add_trace(go.Scatter(
                x=df_filtered.index,
                y=df_filtered["Credit Spread"],
                name="Credit Spread",
                yaxis="y2",
                line=dict(color="blue")
            ))

        if show_signals:
            signal_df = df_filtered[df_filtered["Signal"] == True]
            fig_macro.add_trace(go.Scatter(
                x=signal_df.index,
                y=signal_df["Sentiment"],
                mode="markers",
                name="Predictive Signal",
                marker=dict(color="red", size=10, symbol="circle"),
                hovertemplate="<b>Predictive Signal</b><br>Rising spreads + weak sentiment"
            ))

        # Highlight selloff periods
        selloff_periods = []
        current_period = None
        for i in range(len(df_filtered)):
            if df_filtered["Selloff"].iloc[i]:
                if current_period is None:
                    current_period = [df_filtered.index[i], df_filtered.index[i]]
                else:
                    current_period[1] = df_filtered.index[i]
            elif current_period:
                selloff_periods.append(tuple(current_period))
                current_period = None
        if current_period:
            selloff_periods.append(tuple(current_period))

        for start, end in selloff_periods:
            fig_macro.add_vrect(
                x0=start, x1=end,
                fillcolor="red", opacity=0.2,
                layer="below", line_width=0
            )

        fig_macro.update_layout(
            title="Sentiment and Credit Spreads with S&P 500 Selloffs",
            xaxis=dict(title="Date"),
            yaxis=dict(title="Sentiment", side="left"),
            yaxis2=dict(title="Credit Spread (bps)", overlaying="y", side="right"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig_macro, use_container_width=True)

        # --- SECONDARY RETURNS CHART ---
        if show_returns:
            colors = ["#6b8e23" if val >= 0 else "#8b0000" for val in df_filtered["S&P 500 Returns"]]
            hover_text = [f"{val:+.2f}%" for val in df_filtered["S&P 500 Returns"]]
            fig_returns = go.Figure()
            fig_returns.add_trace(go.Bar(
                x=df_filtered.index,
                y=df_filtered["S&P 500 Returns"],
                name="S&P 500 Returns",
                marker_color=colors,
                text=hover_text,
                hovertemplate="%{text}"
            ))

            fig_returns.update_layout(
                title="S&P 500 Monthly Returns",
                xaxis=dict(title="Date"),
                yaxis=dict(title="Monthly Return", zeroline=True, zerolinecolor="gray"),
                height=300,
                margin=dict(t=50, b=50)
            )

            st.plotly_chart(fig_returns, use_container_width=True)
    else:
        st.warning("No data available in the selected date range. Please adjust the dates.")
