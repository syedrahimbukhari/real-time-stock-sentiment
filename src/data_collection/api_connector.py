from binance.client import Client
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

class BinanceConnector:
    def __init__(self, api_key=None, api_secret=None):
        # Try to get API keys from environment variables or Streamlit secrets
        self.api_key = api_key or os.getenv('BINANCE_API_KEY') 
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        
        # Initialize client with or without API keys
        if self.api_key and self.api_secret:
            self.client = Client(self.api_key, self.api_secret)
            print("✅ Binance API Connected with API Keys")
        else:
            self.client = Client()
            print("ℹ️ Binance API Connected without API Keys (Public Data Only)")
    
    def test_connection(self):
        """Test if we can connect to Binance API"""
        try:
            # Get server time to test connection
            server_time = self.client.get_server_time()
            print("✅ Binance API Connection Successful!")
            
            # Test if we can get account info (if using API keys)
            if self.api_key and self.api_secret:
                try:
                    account_info = self.client.get_account()
                    print("✅ API Keys Verified - Private Data Access Available")
                except Exception as e:
                    print("ℹ️ API Keys working but no trading permissions (as expected)")
            
            return True
        except Exception as e:
            print(f"❌ Connection Failed: {e}")
            return False

# Test with API keys
def test_with_keys():
    """Test connection with API keys from environment"""
    connector = BinanceConnector()
    return connector.test_connection()

if __name__ == "__main__":
    test_with_keys()