#!/usr/bin/env python3
"""
Custom Stock & Crypto Heatmap
Uses yfinance for free price data. No API keys required.
"""

from flask import Flask, jsonify, render_template
import yfinance as yf
import pandas as pd
from datetime import datetime

app = Flask(__name__)

TICKERS = [
    "QQQ", "NVDA", "AVGO", "TSM", "MU", "AMD", "MRVL", "ALAB",
    "ASML", "GOOGL", "TSLA", "SPCX", "PLTR", "SKHY",
    "BTC-USD", "ETH-USD", "SOL-USD", "MSTR"
]

def get_color(pct):
    """Return hex color: full red at -5%, full green at +5%, gray if None."""
    if pct is None or pd.isna(pct):
        return "#6b7280"  # gray-500
    # Clamp
    p = max(-5.0, min(5.0, float(pct)))
    # t: 0 at -5, 1 at +5
    t = (p + 5.0) / 10.0
    r = int(255 * (1 - t))
    g = int(255 * t)
    b = 0
    return f"#{r:02x}{g:02x}{b:02x}"

def fetch_prices():
    """Fetch latest price and 1-day % change for all tickers."""
    results = []
    try:
        # Download recent daily data for all at once
        data = yf.download(TICKERS, period="5d", interval="1d", progress=False, auto_adjust=True)
        if data.empty:
            raise ValueError("No data returned")

        # Handle MultiIndex columns
        closes = data["Close"] if "Close" in data.columns else data

        for ticker in TICKERS:
            try:
                if ticker not in closes.columns:
                    # Try crypto style or fail
                    results.append({
                        "ticker": ticker,
                        "price": None,
                        "change_pct": None,
                        "color": get_color(None)
                    })
                    continue

                series = closes[ticker].dropna()
                if len(series) < 2:
                    results.append({
                        "ticker": ticker,
                        "price": None,
                        "change_pct": None,
                        "color": get_color(None)
                    })
                    continue

                current = float(series.iloc[-1])
                prev = float(series.iloc[-2])
                change_pct = ((current - prev) / prev) * 100 if prev != 0 else None

                results.append({
                    "ticker": ticker,
                    "price": round(current, 2) if current < 1000 else round(current, 0),
                    "change_pct": round(change_pct, 2) if change_pct is not None else None,
                    "color": get_color(change_pct)
                })
            except Exception as e:
                print(f"Error for {ticker}: {e}")
                results.append({
                    "ticker": ticker,
                    "price": None,
                    "change_pct": None,
                    "color": get_color(None)
                })
    except Exception as e:
        print(f"Download failed: {e}")
        # Fallback individual if batch fails
        for ticker in TICKERS:
            results.append({
                "ticker": ticker,
                "price": None,
                "change_pct": None,
                "color": get_color(None)
            })

    return results

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/prices")
def api_prices():
    data = fetch_prices()
    return jsonify({
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tiles": data
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting heatmap server at http://127.0.0.1:{port}")
    print("Open that URL in your browser. Press Ctrl+C to stop.")
    app.run(host="0.0.0.0", port=port, debug=False)
