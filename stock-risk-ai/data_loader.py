import yfinance as yf

def get_data(ticker="AAPL"):
    data = yf.download(ticker, period="max", interval="1d")

    try:
        data.columns = data.columns.get_level_values(0)
    except:
        pass

    data = data[['Close', 'Volume']]
    data.dropna(inplace=True)

    return data