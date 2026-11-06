#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ""
echo "Starting heatmap server..."
echo "Open http://127.0.0.1:5000 in your browser"
echo "Press Ctrl+C to stop"
echo ""

python app.py
