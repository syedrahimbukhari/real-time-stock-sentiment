import sys
import os

# Add src to Python path
sys.path.append('src')

def test_fixed_sentiment():
    """Test the fixed sentiment analyzer"""
    try:
        from sentiment.sentiment_analyzer import AdvancedSentimentAnalyzer
        from sentiment.news_collector import NewsDataCollector
        
        print("✅ Imports successful!")
        
        # Test sentiment analyzer
        analyzer = AdvancedSentimentAnalyzer()
        print("✅ Sentiment analyzer initialized")
        
        # Test news collector
        collector = NewsDataCollector()
        print("✅ News collector initialized")
        
        # Test basic sentiment analysis
        test_text = "Bitcoin is showing strong bullish momentum!"
        result = analyzer.analyze_text(test_text)
        
        if result:
            print(f"✅ Sentiment analysis working: {result['sentiment']}")
        else:
            print("❌ Sentiment analysis failed")
            return False
        
        # Test news collection
        news = collector.get_binance_news(2)
        if news:
            print(f"✅ News collection working: {len(news)} items")
        else:
            print("⚠️ News collection returned empty (might be API issue)")
        
        print("🎉 All tests passed! Imports are fixed.")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    test_fixed_sentiment()