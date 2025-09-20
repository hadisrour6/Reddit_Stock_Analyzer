import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def get_symbol(company_name: str):
    """Search for the stock ticker symbol using a company name."""
    url = f"https://finnhub.io/api/v1/search?q={company_name}&token={API_KEY}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    if data.get("count", 0) > 0:
        return data["result"][0]["symbol"]   # pick the top match
    return None

def get_market_cap(symbol: str):
    """Get market cap given a stock ticker symbol."""
    url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    return int((data.get("marketCapitalization") * 1000000))

def market_cap_formatter(num: float) -> str:
    """Format numbers with commas."""
    return f"{int(num):,}" if num is not None else "N/A"

def get_current_price(symbol:str):
    """Get market cap given a stock ticker symbol."""
    url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    market_cap = float(data.get("marketCapitalization"))
    shares_outstanding = float(data.get("shareOutstanding"))
    return round((market_cap/shares_outstanding),2)
