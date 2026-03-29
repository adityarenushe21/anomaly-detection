Stock Risk Detection using LSTM Autoencoder

This project is a simple attempt to detect unusual behavior in stock data using a deep learning model. Instead of predicting prices, it focuses on identifying when a stock starts behaving differently from its usual pattern.

How it works

The system follows a basic pipeline:

* Fetch stock data
* Create features like returns and volatility
* Normalize the data
* Convert it into sequences
* Train an LSTM autoencoder
* Calculate reconstruction error
* Detect anomalies
* Generate a risk score

Features used

* Close price
* Volume
* Returns (percentage change)
* Volatility

Model

An LSTM autoencoder is used to learn normal patterns in stock data.
If the model is unable to reconstruct the input properly, it means the behavior is unusual.

Anomaly

An anomaly simply means the stock is behaving differently than usual.
This could be due to sudden price movement or increased volatility.

Important:
This model does not predict whether the price will go up or down. It only signals unusual behavior.

Risk Score

The final risk score is based on:

1.anomaly level
2,volatility

Higher score means higher instability.

How to run

Run the following files in order:

python train.py
python test.py
python multi_stock.py

Limitations

1. It is not a trading model
2. Anomaly does not indicate direction
3. Performance can slow down when running many stocks together

Summary

This project helps in identifying unstable or unusual stock behavior and can be used as a basic risk monitoring tool.
