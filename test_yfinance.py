import yfinance as yf

spx = yf.download("^GSPC", start="2004-01-01", end="2024-12-31")
print(spx.head())