from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import joblib
import numpy as np
import pandas as pd
from typing import List, Dict
import yfinance as yf

from model import LSTMAutoencoder
from features import add_features
from prepare import create_sequences
from detect import detect_anomaly
from risk import calculate_risk

app = FastAPI(title="Stock Risk AI API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tickers from multi_stock.py
TICKERS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS",
    "LT.NS", "SBIN.NS", "AXISBANK.NS",
    "KOTAKBANK.NS", "ITC.NS",
    "BAJFINANCE.NS", "MARUTI.NS"
]

def get_stock_data(ticker: str):
    data = yf.download(ticker, period="1y", interval="1d")
    if data.empty:
        return None
    try:
        data.columns = data.columns.get_level_values(0)
    except:
        pass
    data = data[['Close', 'Volume']]
    data.dropna(inplace=True)
    return data

@app.get("/api/stocks")
async def get_all_stocks():
    results = []
    for ticker in TICKERS:
        try:
            data = get_stock_data(ticker)
            if data is None or len(data) < 50:
                continue
            
            data = add_features(data)
            features = data[['Close', 'Volume', 'returns', 'volatility']].values
            
            scaler = joblib.load("scaler.pkl")
            features_scaled = scaler.transform(features)
            X = create_sequences(features_scaled)
            
            errors, anomalies = detect_anomaly(X)
            risk_scores = calculate_risk(errors, data['volatility'].values)
            
            results.append({
                "ticker": ticker,
                "risk_score": float(risk_scores[-1]),
                "is_anomaly": bool(anomalies[-1]),
                "price": float(data['Close'].iloc[-1])
            })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue
    
    return sorted(results, key=lambda x: x['risk_score'])

@app.get("/api/stocks/{ticker}")
async def get_stock_details(ticker: str):
    try:
        data = get_stock_data(ticker)
        if data is None:
            raise HTTPException(status_code=404, detail="Stock not found")
        
        data = add_features(data)
        features = data[['Close', 'Volume', 'returns', 'volatility']].values
        
        scaler = joblib.load("scaler.pkl")
        features_scaled = scaler.transform(features)
        X = create_sequences(features_scaled)
        
        errors, anomalies = detect_anomaly(X)
        risk_scores = calculate_risk(errors, data['volatility'].values)
        
        # Prepare historical data for charts
        # Note: sequences start from index 10 (if seq_len=10)
        history = []
        offset = len(data) - len(errors)
        for i in range(len(errors)):
            idx = i + offset
            history.append({
                "date": data.index[idx].strftime("%Y-%m-%d"),
                "price": float(data['Close'].iloc[idx]),
                "error": float(errors[i]),
                "anomaly": bool(anomalies[i]),
                "volatility": float(data['volatility'].iloc[idx])
            })
            
        return {
            "ticker": ticker,
            "current_risk": float(risk_scores[-1]),
            "is_anomaly": bool(anomalies[-1]),
            "history": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
