def add_features(data):
    data['returns'] = data['Close'].pct_change()
    data['volatility'] = data['returns'].rolling(5).std()
    data = data.dropna()
    return data