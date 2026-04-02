import torch
import joblib
from model import LSTMAutoencoder
from data_loader import get_data
from features import add_features
from prepare import create_sequences
from sklearn.preprocessing import MinMaxScaler

data = get_data("AAPL")
if data.empty:
    print("Error: No data fetched for AAPL. Check yfinance connectivity.")
    exit(1)

data = add_features(data)
if len(data) < 20:
    print(f"Error: Too little data ({len(data)} rows) after feature engineering.")
    exit(1)

features_df = data[['Close','Volume','returns','volatility']]
features = features_df.values

scaler = MinMaxScaler()
features = scaler.fit_transform(features)
joblib.dump(scaler, "scaler.pkl")

X = create_sequences(features)
X_tensor = torch.tensor(X, dtype=torch.float32)

model = LSTMAutoencoder(4, 8)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    output = model(X_tensor)
    loss = torch.mean((output - X_tensor)**2)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print(f"Epoch {epoch}, Loss: {loss.item()}")

torch.save(model.state_dict(), "model.pth")