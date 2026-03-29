import torch
from model import LSTMAutoencoder

def detect_anomaly(X):
    model = LSTMAutoencoder(4, 8)
    model.load_state_dict(torch.load("model.pth"))
    model.eval()

    X_tensor = torch.tensor(X, dtype=torch.float32)

    with torch.no_grad():
        output = model(X_tensor)
        errors = torch.mean((output - X_tensor)**2, dim=(1,2))

    threshold = errors.mean() + 1 * errors.std()

    anomalies = errors > threshold

    return errors, anomalies