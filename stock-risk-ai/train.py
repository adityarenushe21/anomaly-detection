import torch
from model import LSTMAutoencoder
from data_loader import get_data
from features import add_features
from prepare import create_sequences
from sklearn.preprocessing import MinMaxScaler

data = get_data("AAPL")
data = add_features(data)

features = data[['Close','Volume','returns','volatility']].values

scaler = MinMaxScaler()
features = scaler.fit_transform(features)

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