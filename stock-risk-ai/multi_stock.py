import yfinance as yf
from sklearn.preprocessing import MinMaxScaler

from features import add_features
from prepare import create_sequences
from detect import detect_anomaly
from risk import calculate_risk


# 🎯 FINAL 12 STOCKS
tickers = [
    "RELIANCE.NS","TCS.NS","INFY.NS",
    "HDFCBANK.NS","ICICIBANK.NS",
    "LT.NS","SBIN.NS","AXISBANK.NS",
    "KOTAKBANK.NS","ITC.NS",
    "BAJFINANCE.NS","MARUTI.NS"
]


def process_stock(ticker):
    try:
        print(f"\nProcessing {ticker}...")

        data = yf.download(ticker, period="max", interval="1d")

        if data.empty:
            return None

        try:
            data.columns = data.columns.get_level_values(0)
        except:
            pass

        data = data[['Close', 'Volume']]
        data.dropna(inplace=True)

        data = add_features(data)

        if len(data) < 50:
            return None

        features = data[['Close','Volume','returns','volatility']].values

        scaler = MinMaxScaler()
        features = scaler.fit_transform(features)

        X = create_sequences(features)

        errors, anomalies = detect_anomaly(X)

        risk = calculate_risk(errors, data['volatility'].values)

        return float(risk[-1])

    except Exception as e:
        print(f"Error in {ticker}: {e}")
        return None


def analyze_stocks():
    results = {}

    for ticker in tickers:
        risk = process_stock(ticker)

        if risk is not None:
            results[ticker] = risk

    return results


def rank_stocks(results):
    return sorted(results.items(), key=lambda x: x[1])


if __name__ == "__main__":

    results = analyze_stocks()

    print("\n📊 Risk Scores:")
    for stock, score in results.items():
        print(f"{stock}: {score:.2f}")

    ranking = rank_stocks(results)

    print("\n🏆 Ranking (Low → High Risk):")
    for stock, score in ranking:
        print(f"{stock}: {score:.2f}")

    print(f"\n✅ Best Stock (Lowest Risk): {ranking[0][0]}")