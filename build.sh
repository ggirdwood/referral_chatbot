#!/bin/bash
echo "⬇️ Installing dependencies..."
pip install -r requirements.txt

echo "📡 Fetching latest Google Sheets data..."
python export_referrals.py
