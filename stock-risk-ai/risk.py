import numpy as np

def normalize(x):
    return (x - x.min()) / (x.max() - x.min())

def calculate_risk(errors, volatility):
    anomaly_score = normalize(errors.numpy())
    vol_score = normalize(volatility[-len(errors):])

    risk = (0.6 * anomaly_score + 0.4 * vol_score) * 100
    return risk