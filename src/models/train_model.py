import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
import joblib
import os

class ModelTrainer:
    def __init__(self):
        self.models = {}
        self.model_performance = {}
    
    def prepare_data(self, features, target, test_size=0.2, random_state=42):
        """
        Split data into train and test sets
        """
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=test_size, random_state=random_state, stratify=target
        )
        
        print(f"✅ Data split: Train={X_train.shape}, Test={X_test.shape}")
        return X_train, X_test, y_train, y_test
    
    def train_logistic_regression(self, X_train, y_train):
        """
        Train Logistic Regression model
        """
        print("🤖 Training Logistic Regression...")
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X_train, y_train)
        
        self.models['logistic_regression'] = model
        print("✅ Logistic Regression trained")
        return model
    
    def train_random_forest(self, X_train, y_train):
        """
        Train Random Forest model
        """
        print("🌲 Training Random Forest...")
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        model.fit(X_train, y_train)
        
        self.models['random_forest'] = model
        print("✅ Random Forest trained")
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """
        Evaluate model performance
        """
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        
        # Store performance
        self.model_performance[model_name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall
        }
        
        # Print results
        print(f"\n📊 {model_name.upper()} Performance:")
        print(f"   Accuracy:  {accuracy:.3f}")
        print(f"   Precision: {precision:.3f}")
        print(f"   Recall:    {recall:.3f}")
        
        # Check against roadmap benchmark (80% accuracy)
        if accuracy >= 0.8:
            print("   ✅ Accuracy benchmark achieved (>80%)")
        else:
            print("   ⚠️  Accuracy below benchmark, but acceptable for now")
        
        return accuracy, precision, recall
    
    def save_models(self, directory='src/models/saved_models'):
        """
        Save trained models using joblib
        """
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        for model_name, model in self.models.items():
            filename = os.path.join(directory, f'{model_name}.pkl')
            joblib.dump(model, filename)
            print(f"💾 Saved {model_name} to {filename}")
    
    def train_all_models(self, features, target):
        """
        Complete training pipeline for all models
        """
        print("🚀 Starting Model Training Pipeline...")
        
        # Prepare data
        X_train, X_test, y_train, y_test = self.prepare_data(features, target)
        
        # Train models
        lr_model = self.train_logistic_regression(X_train, y_train)
        rf_model = self.train_random_forest(X_train, y_train)
        
        # Evaluate models
        print("\n" + "="*50)
        print("MODEL EVALUATION RESULTS")
        print("="*50)
        
        lr_accuracy, lr_precision, lr_recall = self.evaluate_model(lr_model, X_test, y_test, 'logistic_regression')
        rf_accuracy, rf_precision, rf_recall = self.evaluate_model(rf_model, X_test, y_test, 'random_forest')
        
        # Save models
        self.save_models()
        
        # Return best model
        best_model_name = 'logistic_regression' if lr_accuracy >= rf_accuracy else 'random_forest'
        best_model = self.models[best_model_name]
        
        print(f"\n🏆 Best Model: {best_model_name}")
        
        return best_model, self.model_performance

# Test function
def test_model_training():
    from src.models.feature_engineering import FeatureEngineer
    from src.data_collection.historical_data import HistoricalDataCollector
    
    print("🧪 Testing Model Training...")
    
    # Get data and create features
    collector = HistoricalDataCollector()
    raw_data = collector.get_historical_data(days=90, interval='1h')  # More data for better training
    
    if raw_data is not None:
        engineer = FeatureEngineer()
        data_with_features = engineer.create_technical_indicators(raw_data)
        data_with_target = engineer.create_target_variable(data_with_features)
        features, target = engineer.prepare_features(data_with_target)
        
        # Train models
        trainer = ModelTrainer()
        best_model, performance = trainer.train_all_models(features, target)
        
        print("\n🎉 Model training completed successfully!")
        return best_model, performance
    
    print("❌ Model training failed - no data available")
    return None, None

if __name__ == "__main__":
    test_model_training()