#!/usr/bin/env python3
"""
Custom Stock & Crypto Heatmap
Uses yfinance for free price data. No API keys required.
"""

from flask import Flask, jsonify, render_template, request
import yfinance as yf
import pandas as pd
from datetime import datetime

app = Flask(__name__)

MAIN_TICKERS = [
    "DX-Y.NYB", "^VIX",
    "QQQ", "SMH", "NVDA", "AVGO", "TSM", "MU", "AMD", "MRVL", "ALAB",
    "ASML", "GOOGL", "TSLA", "SPCX", "PLTR", "SKHY",
    "MSTR", "ASST",
    "BTC-USD", "ETH-USD", "SOL-USD", "HYPE32196-USD"
]

MACRO_TICKERS = []

ALL_TICKERS = MAIN_TICKERS + MACRO_TICKERS

def get_color(pct):
    """Bright green if up, red if down, gray if unavailable."""
    if pct is None or pd.isna(pct):
        return "#6b7280"
    if pct > 0:
        return "#4ade80"
    elif pct < 0:
        return "#f87171"
    else:
        return "#9ca3af"

def fetch_prices(period="1d"):
    if period == "1w":
        yf_period = "1mo"
        lookback = 5
    elif period == "1m":
        yf_period = "3mo"
        lookback = 21
    else:
        yf_period = "5d"
        lookback = 1

    results = []
    try:
        data = yf.download(ALL_TICKERS, period=yf_period, interval="1d", progress=False, auto_adjust=True)
        if data.empty:
            raise ValueError("No data returned")

        closes = data["Close"] if "Close" in data.columns else data

        for ticker in ALL_TICKERS:
            try:
                if ticker not in closes.columns:
                    results.append({"ticker": ticker, "price": None, "change_pct": None, "color": get_color(None)})
                    continue

                series = closes[ticker].dropna()
                if len(series) <= lookback:
                    results.append({"ticker": ticker, "price": None, "change_pct": None, "color": get_color(None)})
                    continue

                current = float(series.iloc[-1])
                prev = float(series.iloc[-1 - lookback])
                change_pct = ((current - prev) / prev) * 100 if prev != 0 else None

                results.append({
                    "ticker": ticker,
                    "price": round(current, 2) if current < 1000 else round(current, 0),
                    "change_pct": round(change_pct, 2) if change_pct is not None else None,
                    "color": get_color(change_pct)
                })
            except Exception as e:
                print(f"Error for {ticker}: {e}")
                results.append({"ticker": ticker, "price": None, "change_pct": None, "color": get_color(None)})
    except Exception as e:
        print(f"Download failed: {e}")
        for ticker in ALL_TICKERS:
            results.append({"ticker": ticker, "price": None, "change_pct": None, "color": get_color(None)})

    return results

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/prices")
def api_prices():
    period = request.args.get("period", "1d")
    if period not in ("1d", "1w", "1m"):
        period = "1d"
    data = fetch_prices(period)
    return jsonify({
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "period": period,
        "tiles": data
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
