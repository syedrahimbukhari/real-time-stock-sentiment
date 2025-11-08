import sys
import os

# Add src to Python path
sys.path.append('src')

from data_collection.api_connector import BinanceConnector
from data_collection.live_data import LiveDataCollector
from data_collection.historical_data import HistoricalDataCollector

def test_complete_data_pipeline():
    """Test the complete data collection pipeline"""
    print("🚀 Testing Data Collection Pipeline...\n")
    
    # Test 1: API Connection
    print("1. Testing API Connection...")
    connector = BinanceConnector()
    if not connector.test_connection():
        return False
    
    # Test 2: Live Data
    print("\n2. Testing Live Data Collection...")
    live_collector = LiveDataCollector()
    live_prices = live_collector.get_multiple_prices()
    
    if live_prices:
        for symbol, data in live_prices.items():
            print(f"   ✅ {symbol}: ${data['price']:.2f}")
    else:
        print("   ❌ Live data collection failed")
        return False
    
    # Test 3: Historical Data
    print("\n3. Testing Historical Data Collection...")
    hist_collector = HistoricalDataCollector()
    historical_data = hist_collector.get_historical_data(days=1)  # 1 day for quick test
    
    if historical_data is not None:
        print(f"   ✅ Historical data shape: {historical_data.shape}")
        print(f"   ✅ Columns: {list(historical_data.columns)}")
        
        # Save sample data
        hist_collector.save_historical_data(historical_data, "data/historical/sample_data.csv")
    else:
        print("   ❌ Historical data collection failed")
        return False
    
    print("\n🎉 All data collection tests passed!")
    return True

if __name__ == "__main__":
    test_complete_data_pipeline()