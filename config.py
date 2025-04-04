import os
import streamlit as st
from dotenv import load_dotenv

# Use Streamlit secrets in deployment, fallback to .env locally
if "FRED_API_KEY" in st.secrets:
    FRED_API_KEY = st.secrets["FRED_API_KEY"]
else:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dotenv_path = os.path.join(project_root, ".env")
    load_dotenv(dotenv_path)
    FRED_API_KEY = os.getenv("FRED_API_KEY")

CREDIT_SPREAD_TICKER = "BAMLC0A0CM"
SENTIMENT_TICKER = "UMCSENT"
SP500_TICKER = "SP500"

print("DEBUG - FRED_API_KEY:", FRED_API_KEY)
