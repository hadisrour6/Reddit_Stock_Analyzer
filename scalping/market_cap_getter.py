# import requests
#
#
# def get_market_cap(symbol):
#     url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&interval=5min&apikey=1QJXQB6AM45U1BZE'
#     r = requests.get(url)
#     data = r.json()
#     return data["MarketCapitalization"]
#
# def test(company_name):
#     url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey=1QJXQB6AM45U1BZE"
#     r = requests.get(url)
#     data = r.json()
#     return data
#
# def market_cap_formatter(num):
#     return f"{num:,}"
#
#
import requests

API_KEY = "d2h2st1r01qon4ea8i90d2h2st1r01qon4ea8i9g"

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



get_market_cap("PL")
