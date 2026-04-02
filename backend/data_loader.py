import yfinance as yf
import pandas as pd

def get_data(ticker="AAPL"):
    # Use a specific period and interval to be safe
    df = yf.download(ticker, period="2y", interval="1d", auto_adjust=True)

    if df.empty:
        return pd.DataFrame()

    # Handle cases where yfinance returns MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # We need Close and Volume. yf auto_adjust=True might return 'Close' as the only price.
    required = ['Close', 'Volume']
    available = [c for c in required if c in df.columns]
    
    data = df[available].copy()
    data.dropna(inplace=True)

    return data