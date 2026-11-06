# Custom Stock & Crypto Heatmap

A simple local webpage showing 18 equal-size colored tiles for a custom watchlist of stocks and crypto. Colors run from full red at −5% to full green at +5% based on the one-day price change. Built with Python + yfinance (no API keys needed).

## Tickers

QQQ, NVDA, AVGO, TSM, MU, AMD, MRVL, ALAB, ASML, GOOGL, TSLA, SPCX, PLTR, SKHY, BTC-USD, ETH-USD, SOL-USD, MSTR

## Deploy it free (recommended)

See **DEPLOY.md** for step-by-step instructions to put this on Render’s free tier. You’ll get a public URL you can open every morning.

## Run locally

1. Open a terminal and go into this folder:
   ```bash
   cd stock_heatmap
   ```

2. Make the script executable (only needed once):
   ```bash
   chmod +x run.sh
   ```

3. Launch everything with one command:
   ```bash
   ./run.sh
   ```

4. Open **http://127.0.0.1:5000**

Click the **Refresh** button anytime to reload the latest prices.

## Requirements

- Python 3.9+
- Internet connection (yfinance downloads data from Yahoo Finance)

## Notes

- Gray tiles mean data was unavailable for that ticker.
- Prices and changes are based on the most recent daily closes (previous close vs. latest close).
- Crypto tickers use the `-USD` suffix supported by Yahoo Finance.
- To stop the server, press `Ctrl+C` in the terminal.

Enjoy your morning heatmap!
