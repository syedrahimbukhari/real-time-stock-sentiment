from binance.client import Client
import os

# Test connection (without real keys first)
client = Client()

# Get BTC price
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
print(f"Current BTC Price: {btc_price['price']}")
