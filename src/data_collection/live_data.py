import time
from datetime import datetime
import pandas as pd
from .api_connector import BinanceConnector

class LiveDataCollector:
    def __init__(self, api_key=None, api_secret=None):
        self.connector = BinanceConnector(api_key, api_secret)
        self.data_history = {}
        self.max_history = 100  # Maximum data points to keep
    
    def get_current_price(self, symbol='BTCUSDT'):
        """Get current price for a symbol"""
        try:
            ticker = self.connector.client.get_symbol_ticker(symbol=symbol)
            
            price_data = {
                'symbol': symbol,
                'price': float(ticker['price']),
                'timestamp': datetime.now()
            }
            
            # Update history
            if symbol not in self.data_history:
                self.data_history[symbol] = []
            
            self.data_history[symbol].append(price_data)
            
            # Keep only recent data
            if len(self.data_history[symbol]) > self.max_history:
                self.data_history[symbol].pop(0)
            
            return price_data
            
        except Exception as e:
            print(f"Error getting price for {symbol}: {e}")
            return None
    
    def get_price_history(self, symbol='BTCUSDT'):
        """Get price history for a symbol"""
        return self.data_history.get(symbol, [])
    
    def get_multiple_prices(self, symbols=['BTCUSDT', 'ETHUSDT', 'ADAUSDT']):
        """Get prices for multiple cryptocurrencies"""
        prices = {}
        for symbol in symbols:
            price_data = self.get_current_price(symbol)
            if price_data:
                prices[symbol] = price_data
        return prices
    
    def get_historical_klines(self, symbol='BTCUSDT', interval='1m', limit=100):
        """Get recent kline data for real-time analysis"""
        try:
            klines = self.connector.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            # Convert to DataFrame
            columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume',
                      'close_time', 'quote_volume', 'trades', 
                      'taker_buy_base', 'taker_buy_quote', 'ignore']
            
            df = pd.DataFrame(klines, columns=columns)
            
            # Convert data types
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_cols] = df[numeric_cols].astype(float)
            
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
        except Exception as e:
            print(f"Error getting klines for {symbol}: {e}")
            return None

# Test enhanced live data
def test_enhanced_live_data():
    collector = LiveDataCollector()
    
    print("🚀 Testing Enhanced Live Data Collection...")
    
    # Test current price
    btc_price = collector.get_current_price('BTCUSDT')
    if btc_price:
        print(f"✅ Live BTC Price: ${btc_price['price']:.2f}")
    
    # Test price history
    history = collector.get_price_history('BTCUSDT')
    print(f"✅ Price History Length: {len(history)}")
    
    # Test klines data
    klines = collector.get_historical_klines('BTCUSDT', '1m', 10)
    if klines is not None:
        print(f"✅ Klines Data Shape: {klines.shape}")
    
    return collector

if __name__ == "__main__":
    test_enhanced_live_data()