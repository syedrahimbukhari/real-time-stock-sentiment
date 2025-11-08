from textblob import TextBlob

class SimpleSentimentAnalyzer:
    def __init__(self):
        print("✅ Simple Sentiment Analyzer Initialized")
    
    def analyze_text(self, text):
        """
        Simple sentiment analysis using TextBlob
        Returns: sentiment ('Positive', 'Negative', 'Neutral') and polarity score
        """
        try:
            # Create TextBlob object
            analysis = TextBlob(str(text))
            
            # Get polarity score (-1 to 1)
            polarity = analysis.sentiment.polarity
            
            # Determine sentiment
            if polarity > 0.1:
                sentiment = "Positive"
            elif polarity < -0.1:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            
            return {
                'text': text,
                'polarity': round(polarity, 3),
                'sentiment': sentiment
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return None
    
    def analyze_multiple(self, texts):
        """Analyze multiple texts"""
        results = []
        for text in texts:
            result = self.analyze_text(text)
            if result:
                results.append(result)
        return results

# Test function as per roadmap
def test_sentiment():
    analyzer = SimpleSentimentAnalyzer()
    
    # Test with sample financial comments (as mentioned in roadmap)
    sample_comments = [
        "Bitcoin price is going up! Great investment!",
        "Market is crashing, I'm losing money",
        "The crypto market is stable today",
        "This is terrible news for investors",
        "Amazing growth in blockchain technology"
    ]
    
    print("🧪 Testing Sentiment Analysis with Sample Comments:\n")
    
    for comment in sample_comments:
        result = analyzer.analyze_text(comment)
        if result:
            print(f"💬 Comment: {result['text']}")
            print(f"🎯 Sentiment: {result['sentiment']}")
            print(f"📊 Polarity Score: {result['polarity']}")
            print("-" * 40)

if __name__ == "__main__":
    test_sentiment()