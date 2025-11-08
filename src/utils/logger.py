import logging
import os
import pandas as pd
from datetime import datetime
import json
import sys

class ProjectLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration with Unicode support"""
        # Create logs directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Configure logging with UTF-8 encoding
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                # File handler with UTF-8 encoding
                logging.FileHandler(f"{self.log_dir}/app.log", encoding='utf-8'),
                # Custom stream handler for Windows compatibility
                self._get_safe_stream_handler()
            ]
        )
        
        self.logger = logging.getLogger("StockSentimentTracker")
        self.logger.info("Logger initialized successfully")
    
    def _get_safe_stream_handler(self):
        """Create a stream handler that safely handles Unicode on Windows"""
        class SafeStreamHandler(logging.StreamHandler):
            def emit(self, record):
                try:
                    msg = self.format(record)
                    # Encode to UTF-8 and replace any problematic characters
                    msg = msg.encode('utf-8', 'replace').decode('utf-8')
                    stream = self.stream
                    stream.write(msg + self.terminator)
                    self.flush()
                except Exception:
                    self.handleError(record)
        
        return SafeStreamHandler()
    
    def log_user_interaction(self, action, details):
        """Log user interactions"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details
        }
        
        # Use text instead of emojis for Windows compatibility
        self.logger.info(f"USER_ACTION: {action} - {details}")
        
        # Save to CSV for analytics
        self._save_to_csv('user_interactions', log_entry)
        
        return log_entry
    
    def log_prediction(self, symbol, prediction_result, features_used=None):
        """Log ML predictions"""
        # Convert movement emoji to text for logging
        movement = prediction_result.get('movement', 'N/A')
        movement_text = movement.replace('📈', 'UP').replace('📉', 'DOWN')
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol,
            'prediction': prediction_result.get('prediction', 'N/A'),
            'movement': movement_text,
            'confidence': prediction_result.get('confidence', 0),
            'probability_up': prediction_result.get('probability_up', 0),
            'probability_down': prediction_result.get('probability_down', 0),
            'features_used': features_used or []
        }
        
        self.logger.info(f"PREDICTION: {symbol} - {movement_text} - Confidence: {prediction_result.get('confidence', 0):.3f}")
        
        # Save to CSV for model monitoring
        self._save_to_csv('predictions', log_entry)
        
        return log_entry
    
    def log_sentiment_analysis(self, text, sentiment_result):
        """Log sentiment analysis results"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'text_preview': text[:100] + "..." if len(text) > 100 else text,
            'sentiment': sentiment_result.get('sentiment', 'N/A'),
            'polarity': sentiment_result.get('polarity', 0),
            'text_length': len(text)
        }
        
        self.logger.info(f"SENTIMENT: {sentiment_result.get('sentiment', 'N/A')} - Polarity: {sentiment_result.get('polarity', 0):.3f}")
        
        # Save to CSV for sentiment tracking
        self._save_to_csv('sentiment_analysis', log_entry)
        
        return log_entry
    
    def log_error(self, error_type, error_message, context=None):
        """Log errors with context"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'error_message': error_message,
            'context': context or {}
        }
        
        self.logger.error(f"ERROR: {error_type} - {error_message}")
        
        # Save to CSV for error analysis
        self._save_to_csv('errors', log_entry)
        
        return log_entry
    
    def log_performance(self, operation, duration, details=None):
        """Log performance metrics"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'duration_seconds': duration,
            'details': details or {}
        }
        
        self.logger.info(f"PERFORMANCE: {operation} - {duration:.3f}s")
        
        # Save to CSV for performance monitoring
        self._save_to_csv('performance', log_entry)
        
        return log_entry
    
    def _save_to_csv(self, log_type, log_entry):
        """Save log entry to CSV file with UTF-8 encoding"""
        try:
            csv_file = f"{self.log_dir}/{log_type}.csv"
            
            # Convert to DataFrame
            df = pd.DataFrame([log_entry])
            
            # Append to existing file or create new (with UTF-8 encoding)
            if os.path.exists(csv_file):
                existing_df = pd.read_csv(csv_file)
                updated_df = pd.concat([existing_df, df], ignore_index=True)
                updated_df.to_csv(csv_file, index=False, encoding='utf-8')
            else:
                df.to_csv(csv_file, index=False, encoding='utf-8')
                
        except Exception as e:
            self.logger.error(f"Failed to save log to CSV: {e}")
    
    def get_log_summary(self):
        """Get summary of all logs"""
        summary = {
            'total_user_interactions': 0,
            'total_predictions': 0,
            'total_sentiment_analysis': 0,
            'total_errors': 0,
            'recent_activity': []
        }
        
        try:
            log_files = {
                'user_interactions': 'user_interactions.csv',
                'predictions': 'predictions.csv',
                'sentiment_analysis': 'sentiment_analysis.csv',
                'errors': 'errors.csv'
            }
            
            for log_type, filename in log_files.items():
                csv_file = f"{self.log_dir}/{filename}"
                if os.path.exists(csv_file):
                    df = pd.read_csv(csv_file, encoding='utf-8')
                    summary[f'total_{log_type}'] = len(df)
                    
                    # Get recent activity
                    if len(df) > 0:
                        recent = df.tail(3).to_dict('records')
                        summary['recent_activity'].extend(recent)
        
        except Exception as e:
            self.logger.error(f"Failed to generate log summary: {e}")
        
        return summary

# Test function with Windows compatibility
def test_logger():
    """Test the logging system with Windows compatibility"""
    print("Testing Logger with Windows Compatibility...")
    
    logger = ProjectLogger("test_logs")
    
    # Test different log types (without emojis for Windows)
    logger.log_user_interaction("page_visit", {"page": "dashboard", "user_agent": "test"})
    logger.log_sentiment_analysis("Bitcoin is amazing!", {"sentiment": "Positive", "polarity": 0.8})
    
    # Use text instead of emojis for movement
    logger.log_prediction("BTCUSDT", {"movement": "UP", "confidence": 0.75})
    logger.log_performance("data_fetch", 0.45, {"symbols": 3})
    
    # Test error logging
    try:
        raise ValueError("Test error for logging")
    except Exception as e:
        logger.log_error("ValueError", str(e), {"context": "test_scenario"})
    
    # Get summary
    summary = logger.get_log_summary()
    print(f"Log Summary: {summary}")
    
    print("Logger test completed successfully")
    return logger

if __name__ == "__main__":
    test_logger()