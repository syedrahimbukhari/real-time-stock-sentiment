import joblib
import pandas as pd
import numpy as np
from datetime import datetime

class PricePredictor:
    def __init__(self, model_path=None):
        self.model = None
        self.feature_columns = None
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """
        Load trained model from file
        """
        try:
            self.model = joblib.load(model_path)
            print(f"✅ Model loaded from {model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
    
    def prepare_live_features(self, historical_data, feature_engineer):
        """
        Prepare features from live/historical data for prediction
        """
        # Create technical indicators
        data_with_features = feature_engineer.create_technical_indicators(historical_data)
        
        # Get the latest row for prediction
        latest_data = data_with_features.iloc[-1:].copy()
        
        # Prepare features (exclude non-feature columns)
        feature_columns = [col for col in latest_data.columns if col not in 
                         ['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        
        features = latest_data[feature_columns]
        
        # Handle NaN values
        features = features.fillna(0)
        
        return features, feature_columns
    
    def predict_price_movement(self, historical_data, feature_engineer):
        """
        Predict whether price will increase in next period
        """
        if self.model is None:
            return {"error": "No model loaded"}
        
        try:
            # Prepare features
            features, feature_columns = self.prepare_live_features(historical_data, feature_engineer)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            prediction_proba = self.model.predict_proba(features)[0]
            
            # Interpret results
            confidence = prediction_proba[prediction]
            movement = "UP 📈" if prediction == 1 else "DOWN 📉"
            
            result = {
                'prediction': prediction,
                'movement': movement,
                'confidence': round(confidence, 3),
                'probability_up': round(prediction_proba[1], 3),
                'probability_down': round(prediction_proba[0], 3),
                'timestamp': datetime.now()
            }
            
            return result
            
        except Exception as e:
            return {"error": f"Prediction failed: {e}"}

# Test function
def test_prediction():
    from src.models.feature_engineering import FeatureEngineer
    from src.data_collection.historical_data import HistoricalDataCollector
    
    print("🧪 Testing Prediction...")
    
    # Get recent data
    collector = HistoricalDataCollector()
    recent_data = collector.get_historical_data(days=10, interval='1h')
    
    if recent_data is not None:
        # Initialize predictor with best model
        predictor = PricePredictor('src/models/saved_models/random_forest.pkl')
        feature_engineer = FeatureEngineer()
        
        # Make prediction
        prediction_result = predictor.predict_price_movement(recent_data, feature_engineer)
        
        print("\n🎯 PREDICTION RESULT:")
        print(f"Movement: {prediction_result.get('movement', 'N/A')}")
        print(f"Confidence: {prediction_result.get('confidence', 'N/A')}")
        print(f"Probability UP: {prediction_result.get('probability_up', 'N/A')}")
        print(f"Probability DOWN: {prediction_result.get('probability_down', 'N/A')}")
        
        return prediction_result
    
    return None

if __name__ == "__main__":
    test_prediction()