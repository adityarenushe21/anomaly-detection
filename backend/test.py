from data_loader import get_data
from features import add_features
from prepare import create_sequences
from detect import detect_anomaly
from risk import calculate_risk
import joblib

# Load data
data = get_data()
data = add_features(data)

# 🔥 LOAD SAVED SCALER
scaler = joblib.load("scaler.pkl")

features = data[['Close','Volume','returns','volatility']].values
features = scaler.transform(features)

# Create sequences
X = create_sequences(features)

# Detect anomaly
errors, anomalies = detect_anomaly(X)

print("Total anomalies:", anomalies.sum())

# Risk score
risk = calculate_risk(errors, data['volatility'].values)

print("Risk Score:", risk[-1])
print("Is Anomaly:", anomalies[-1])