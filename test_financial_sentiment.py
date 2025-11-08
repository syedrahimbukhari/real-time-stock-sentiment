import sys
sys.path.append('src')

from sentiment.sentiment_analyzer import SimpleSentimentAnalyzer

def test_with_financial_comments():
    """Test sentiment analysis with financial comments"""
    analyzer = SimpleSentimentAnalyzer()
    
    # Sample financial comments (you can add your friends' comments here)
    financial_comments = [
        "BTC to the moon! 🚀",
        "Market is so bearish right now",
        "Just bought more Ethereum, feeling bullish",
        "Crypto crash incoming, be careful",
        "Stable market conditions today",
        "Great news for Bitcoin investors!",
        "I'm worried about this downturn",
        "Perfect time to buy the dip",
        "Market sentiment is neutral currently",
        "Bull run starting soon!"
    ]
    
    print("💰 Testing with Financial Comments:\n")
    
    results = analyzer.analyze_multiple(financial_comments)
    
    # Display results
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for result in results:
        print(f"💬 {result['text']}")
        print(f"   → Sentiment: {result['sentiment']} (Score: {result['polarity']})")
        
        # Count sentiments
        if result['sentiment'] == "Positive":
            positive_count += 1
        elif result['sentiment'] == "Negative":
            negative_count += 1
        else:
            neutral_count += 1
    
    # Summary
    print("\n📈 SENTIMENT SUMMARY:")
    print(f"Positive Comments: {positive_count}")
    print(f"Negative Comments: {negative_count}") 
    print(f"Neutral Comments: {neutral_count}")
    print(f"Total Comments: {len(results)}")
    
    # Calculate accuracy (manual check)
    print("\n✅ Manual Accuracy Check:")
    print("Please verify if the sentiments make sense for financial context")
    
    return results

if __name__ == "__main__":
    test_with_financial_comments()