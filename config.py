from dotenv import load_dotenv
import os
import streamlit as st  # NEW

# Use Streamlit secrets if deployed on Streamlit Cloud
if "FRED_API_KEY" in st.secrets:
    FRED_API_KEY = st.secrets["FRED_API_KEY"]
else:
    # Local .env
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(dotenv_path)
    FRED_API_KEY = os.getenv("FRED_API_KEY")