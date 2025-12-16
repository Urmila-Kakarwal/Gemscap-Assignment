# Gemscap-Assignment
Real-Time Quant Analytics Dashboard
Overview

A real-time quantitative analytics dashboard for live crypto markets.
The application streams BTCUSDT and ETHUSDT prices, computes spread and rolling z-score, and visualizes relative-value signals through an interactive interface.

Features

Live BTC & ETH price monitoring (1s refresh)

Interactive price charts

Spread and rolling z-score calculation

Configurable alert thresholds

Visual alert markers on z-score chart

CSV export of processed data

Tech Stack

Python

Streamlit

Pandas / NumPy

Altair

Binance REST API

Run Locally
Install Dependencies
pip install streamlit pandas numpy altair requests streamlit-autorefresh

Start Application
streamlit run app.py

How It Works

Fetches live BTCUSDT and ETHUSDT prices from Binance

Accumulates data in session state

Computes spread and rolling z-score

Updates charts and alerts in near real-time

Allows CSV download for offline analysis

Future Extensions

WebSocket-based ingestion

Hedge ratio estimation (OLS / Kalman)

ADF test and rolling correlation

Multi-timeframe resampling
