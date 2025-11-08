import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class FeatureEngineer:
    def __init__(self):
        print("✅ Feature Engineer Initialized")
    
    def create_technical_indicators(self, df):
        """
        Create technical indicators from price data
        """
        # Make a copy to avoid modifying original data
        data = df.copy()
        
        # 1. Price-based features
        data['price_change'] = data['close'].pct_change()
        data['high_low_ratio'] = data['high'] / data['low']
        data['open_close_ratio'] = data['open'] / data['close']
        
        # 2. Moving Averages (as mentioned in roadmap)
        data['ma_5'] = data['close'].rolling(window=5).mean()      # 5-minute equivalent
        data['ma_15'] = data['close'].rolling(window=15).mean()    # 15-minute equivalent
        data['ma_30'] = data['close'].rolling(window=30).mean()    # 30-minute equivalent
        
        # 3. Moving Average Ratios
        data['ma_ratio_5_15'] = data['ma_5'] / data['ma_15']
        data['ma_ratio_15_30'] = data['ma_15'] / data['ma_30']
        
        # 4. Volatility (as mentioned in roadmap)
        data['volatility_5'] = data['close'].rolling(window=5).std()
        data['volatility_15'] = data['close'].rolling(window=15).std()
        
        # 5. Price Position relative to MAs
        data['price_vs_ma5'] = data['close'] / data['ma_5']
        data['price_vs_ma15'] = data['close'] / data['ma_15']
        
        # 6. Volume features
        data['volume_change'] = data['volume'].pct_change()
        data['volume_ma_5'] = data['volume'].rolling(window=5).mean()
        
        print(f"✅ Created {len([col for col in data.columns if col not in ['timestamp', 'open', 'high', 'low', 'close', 'volume']])} technical indicators")
        return data
    
    def create_target_variable(self, df, lookahead_periods=4, threshold=0.01):
        """
        Create target variable for binary classification
        As per roadmap: "Agley 1 ghante mein price 1% se zyada barhay ga ya nahi?"
        
        For hourly data, lookahead_periods=4 means 4 hours ahead
        """
        data = df.copy()
        
        # Calculate future price (4 periods ahead for 1-hour data = 4 hours)
        data['future_close'] = data['close'].shift(-lookahead_periods)
        
        # Calculate future return
        data['future_return'] = (data['future_close'] - data['close']) / data['close']
        
        # Create binary target: 1 if price increases by threshold (1%), else 0
        data['target'] = (data['future_return'] > threshold).astype(int)
        
        # Remove rows with NaN values (end of dataset)
        data = data.dropna()
        
        print(f"✅ Target variable created: {data['target'].value_counts().to_dict()}")
        return data
    
    def prepare_features(self, df):
        """
        Prepare final feature set for modeling
        """
        # Select only feature columns (exclude target, timestamp, and raw price columns)
        feature_columns = [col for col in df.columns if col not in 
                         ['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                          'future_close', 'future_return', 'target']]
        
        features = df[feature_columns]
        target = df['target']
        
        print(f"✅ Final feature set: {len(feature_columns)} features")
        print(f"Features: {feature_columns}")
        
        return features, target

# Test function
def test_feature_engineering():
    # Load sample data (from Phase 1)
    import sys
    import os
    sys.path.append('..')
    
    from src.data_collection.historical_data import HistoricalDataCollector
    
    print("🧪 Testing Feature Engineering...")
    
    # Get historical data
    collector = HistoricalDataCollector()
    data = collector.get_historical_data(days=90, interval='1h')
    
    if data is not None:
        # Initialize feature engineer
        engineer = FeatureEngineer()
        
        # Create technical indicators
        data_with_indicators = engineer.create_technical_indicators(data)
        
        # Create target variable
        data_with_target = engineer.create_target_variable(data_with_indicators)
        
        # Prepare features
        features, target = engineer.prepare_features(data_with_target)
        
        print(f"📊 Final dataset shape: {features.shape}")
        print(f"🎯 Target distribution: {target.value_counts()}")
        
        return features, target
    
    return None, None

if __name__ == "__main__":
    test_feature_engineering()