# 📉 Macro Risk Visualizer

This interactive Streamlit app visualizes the relationship between investment-grade credit spreads, consumer sentiment, and S&P 500 market selloffs. It highlights periods of significant drawdowns and explores whether shifts in credit sentiment can serve as early warning signals for equity volatility.

---

## 🔍 Features

- **Dual-axis macro chart** with:
  - Investment-grade credit spreads (right Y-axis)
  - Consumer sentiment (left Y-axis)
  - Predictive signal markers
  - Selloff zones (highlighted in red)

- **Zero-centered bar chart** of monthly S&P 500 returns with:
  - Green/red color coding
  - Tooltip showing percentage change
  - Separately displayed to reduce clutter

- **Toggle controls** for sentiment, spreads, returns, and signals

---

## 📊 Data Sources

- **FRED API** for:
  - Credit Spreads: ICE BofA US Corporate Index Option-Adjusted Spread (`BAMLC0A0CM`)
  - Consumer Sentiment: University of Michigan Sentiment Index (`UMCSENT`)
  - S&P 500 Index: Monthly closing values and return series (`SP500`)

---

## 🚀 Deployment

This app is built using:

- `Streamlit` for the UI
- `Plotly` for interactive charts
- `Pandas` for data handling
- `FRED API` (via `fredapi` package)

To run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
