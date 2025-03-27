from fredapi import Fred
import os
from dotenv import load_dotenv

load_dotenv()
fred = Fred(api_key=os.getenv("FRED_API_KEY"))

data = fred.get_series("UMCSENT")
print(data.tail())
