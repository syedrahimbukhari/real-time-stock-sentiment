import pandas as pd
from .api_connector import BinanceConnector

class HistoricalDataCollector:
    def __init__(self, api_key=None, api_secret=None):
        self.connector = BinanceConnector(api_key, api_secret)

    
    def get_historical_data(self, symbol='BTCUSDT', interval='1h', days=90):
        """Fetch 90 days of historical data for analysis and modeling"""
        try:
            # Calculate start date
            start_str = f"{days} days ago UTC"
            
            # Get historical klines data
            klines = self.connector.client.get_historical_klines(
                symbol=symbol,
                interval=interval,
                start_str=start_str
            )
            
            # Define columns
            columns = [
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades',
                'taker_buy_base', 'taker_buy_quote', 'ignore'
            ]
            
            # Create DataFrame
            df = pd.DataFrame(klines, columns=columns)
            
            # Convert data types
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_volume']
            df[numeric_cols] = df[numeric_cols].astype(float)
            
            # Keep only essential columns
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
            print(f"✅ Downloaded {len(df)} records for {symbol}")
            return df
            
        except Exception as e:
            print(f"❌ Error downloading historical data: {e}")
            return None
    
    def save_historical_data(self, df, filename=None):
        """Save historical data to CSV"""
        if filename is None:
            filename = f"data/historical/btc_historical_{pd.Timestamp.now().strftime('%Y%m%d')}.csv"
        
        df.to_csv(filename, index=False)
        print(f"💾 Data saved to: {filename}")

# Test function
def test_historical_data():
    collector = HistoricalDataCollector()
    
    # Get 90 days of data for testing
    btc_data = collector.get_historical_data(days=90)
    
    if btc_data is not None:
        print(f"📈 Data Shape: {btc_data.shape}")
        print(f"📅 Date Range: {btc_data['timestamp'].min()} to {btc_data['timestamp'].max()}")
        print(f"💰 Price Range: ${btc_data['close'].min():.2f} - ${btc_data['close'].max():.2f}")
        
        # Save data
        collector.save_historical_data(btc_data)
        
        return btc_data
    return None

if __name__ == "__main__":
    test_historical_data()
