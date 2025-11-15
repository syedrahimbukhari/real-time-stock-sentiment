from textblob import TextBlob
import pandas as pd
from datetime import datetime
from typing import Dict, List
import sys
import os

# Fix imports - try both relative and absolute
try:
    # When running as part of package
    from .news_collector import NewsDataCollector
except ImportError:
    try:
        # When running directly
        from news_collector import NewsDataCollector
    except ImportError:
        # Final fallback - add to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
        from sentiment.news_collector import NewsDataCollector

class AdvancedSentimentAnalyzer:
    def __init__(self):
        print("✅ Advanced Sentiment Analyzer Initialized")
        self.news_collector = NewsDataCollector()
        
        # Enhanced financial lexicon with weights
        self.financial_lexicon = {
            "strong_positive": {
                "words": ["moon", "rocket", "bullish", "breakout", "surge", "rally", "pump", "explosion"],
                "weight": 0.8
            },
            "positive": {
                "words": ["buy", "growth", "profit", "gain", "success", "recovery", "optimistic", "bull"],
                "weight": 0.4
            },
            "negative": {
                "words": ["sell", "loss", "drop", "warning", "risk", "fear", "caution", "concern", "bear"],
                "weight": -0.4
            },
            "strong_negative": {
                "words": ["crash", "dump", "collapse", "disaster", "panic", "bloodbath", "rekt", "bearish"],
                "weight": -0.8
            },
            "technical_positive": {
                "words": ["support", "accumulation", "breakout", "uptrend", "resistance broken", "bull flag"],
                "weight": 0.6
            },
            "technical_negative": {
                "words": ["resistance", "liquidation", "breakdown", "downtrend", "support broken", "bear flag"],
                "weight": -0.6
            }
        }

    def analyze_text(self, text: str) -> Dict:
        """
        Advanced financial sentiment analysis
        """
        try:
            text_str = str(text).lower()
            
            # Base sentiment from TextBlob
            analysis = TextBlob(text_str)
            base_polarity = analysis.sentiment.polarity
            base_subjectivity = analysis.sentiment.subjectivity
            
            # Financial keyword analysis
            financial_score = 0
            keyword_matches = {}
            
            for category, data in self.financial_lexicon.items():
                matches = [word for word in data['words'] if word in text_str]
                if matches:
                    keyword_matches[category] = matches
                    financial_score += data['weight'] * len(matches)
            
            # Combine base polarity with financial score
            # Financial keywords have stronger influence
            combined_polarity = base_polarity + (financial_score * 0.3)
            combined_polarity = max(min(combined_polarity, 1.0), -1.0)
            
            # Determine sentiment with financial context
            if combined_polarity > 0.25:
                sentiment = "STRONGLY BULLISH"
                emoji = "🚀"
            elif combined_polarity > 0.1:
                sentiment = "BULLISH" 
                emoji = "📈"
            elif combined_polarity < -0.25:
                sentiment = "STRONGLY BEARISH"
                emoji = "🐻"
            elif combined_polarity < -0.1:
                sentiment = "BEARISH"
                emoji = "📉"
            else:
                sentiment = "NEUTRAL"
                emoji = "⚖️"
            
            # Confidence based on subjectivity and keyword matches
            confidence = min((abs(combined_polarity) + (len(keyword_matches) * 0.2)), 1.0)
            
            return {
                'text': text,
                'sentiment': sentiment,
                'emoji': emoji,
                'polarity': round(combined_polarity, 3),
                'confidence': round(confidence, 3),
                'base_polarity': round(base_polarity, 3),
                'financial_score': round(financial_score, 3),
                'subjectivity': round(base_subjectivity, 3),
                'keyword_matches': keyword_matches,
                'total_keywords': len(keyword_matches)
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return None

    def analyze_news_source(self, source_data: List[Dict]) -> Dict:
        """
        Analyze sentiment for a specific news source
        """
        if not source_data:
            return None
            
        sentiments = []
        total_items = len(source_data)
        
        for item in source_data:
            text = item.get('title', '') + ' ' + item.get('content', '')
            sentiment_result = self.analyze_text(text)
            
            if sentiment_result:
                sentiments.append(sentiment_result)
        
        if not sentiments:
            return None
        
        # Calculate average sentiment for the source
        avg_polarity = sum(s['polarity'] for s in sentiments) / len(sentiments)
        avg_confidence = sum(s['confidence'] for s in sentiments) / len(sentiments)
        
        # Determine overall sentiment
        if avg_polarity > 0.2:
            overall_sentiment = "BULLISH"
        elif avg_polarity > 0.05:
            overall_sentiment = "SLIGHTLY BULLISH"
        elif avg_polarity < -0.2:
            overall_sentiment = "BEARISH" 
        elif avg_polarity < -0.05:
            overall_sentiment = "SLIGHTLY BEARISH"
        else:
            overall_sentiment = "NEUTRAL"
        
        return {
            'source': source_data[0].get('source', 'unknown'),
            'overall_sentiment': overall_sentiment,
            'average_polarity': round(avg_polarity, 3),
            'average_confidence': round(avg_confidence, 3),
            'total_articles': total_items,
            'analyzed_articles': len(sentiments),
            'sentiment_breakdown': {
                'BULLISH': len([s for s in sentiments if s['polarity'] > 0.1]),
                'NEUTRAL': len([s for s in sentiments if -0.1 <= s['polarity'] <= 0.1]),
                'BEARISH': len([s for s in sentiments if s['polarity'] < -0.1])
            },
            'sample_articles': source_data[:3]  # First 3 articles for display
        }

    def compare_sources_sentiment(self, crypto_symbol: str = "BTC") -> Dict:
        """
        Compare sentiment across different news sources
        """
        print(f"🔍 Comparing sentiment across sources for {crypto_symbol}...")
        
        # Collect news from all sources
        all_news = self.news_collector.collect_all_news(crypto_symbol)
        
        if not all_news:
            print("❌ No news collected for comparison")
            return None
        
        # Group news by source
        news_by_source = {}
        for news in all_news:
            source = news.get('source')
            if source not in news_by_source:
                news_by_source[source] = []
            news_by_source[source].append(news)
        
        # Analyze each source
        source_analysis = {}
        for source, news_list in news_by_source.items():
            analysis = self.analyze_news_source(news_list)
            if analysis:
                source_analysis[source] = analysis
        
        # Calculate overall market sentiment
        if source_analysis:
            total_polarity = sum(analysis['average_polarity'] for analysis in source_analysis.values())
            overall_polarity = total_polarity / len(source_analysis)
            
            if overall_polarity > 0.15:
                market_sentiment = "BULLISH 📈"
            elif overall_polarity > 0.05:
                market_sentiment = "SLIGHTLY BULLISH ↗️"
            elif overall_polarity < -0.15:
                market_sentiment = "BEARISH 📉" 
            elif overall_polarity < -0.05:
                market_sentiment = "SLIGHTLY BEARISH ↘️"
            else:
                market_sentiment = "NEUTRAL ⚖️"
        else:
            market_sentiment = "UNKNOWN"
            overall_polarity = 0
        
        return {
            'crypto_symbol': crypto_symbol,
            'market_sentiment': market_sentiment,
            'overall_polarity': round(overall_polarity, 3),
            'sources_analyzed': len(source_analysis),
            'source_analysis': source_analysis,
            'analysis_time': datetime.now()
        }

    def get_sentiment_summary(self, crypto_symbol: str = "BTC") -> Dict:
        """
        Get a comprehensive sentiment summary
        """
        comparison = self.compare_sources_sentiment(crypto_symbol)
        
        if not comparison:
            return None
        
        # Create summary
        summary = {
            'symbol': crypto_symbol,
            'market_sentiment': comparison['market_sentiment'],
            'overall_polarity': comparison['overall_polarity'],
            'source_count': comparison['sources_analyzed'],
            'analysis_time': comparison['analysis_time'],
            'source_details': []
        }
        
        for source, analysis in comparison['source_analysis'].items():
            summary['source_details'].append({
                'source': source.upper(),
                'sentiment': analysis['overall_sentiment'],
                'polarity': analysis['average_polarity'],
                'confidence': analysis['average_confidence'],
                'articles_analyzed': analysis['analyzed_articles']
            })
        
        return summary

# Test function
def test_advanced_sentiment():
    """Test the advanced sentiment analyzer"""
    print("🧪 Testing Advanced Sentiment Analysis...")
    
    analyzer = AdvancedSentimentAnalyzer()
    
    # Test single text analysis
    test_text = "Bitcoin is showing strong bullish momentum with institutional adoption increasing! Technical analysis indicates potential breakout above resistance levels. 🚀"
    result = analyzer.analyze_text(test_text)
    
    print(f"📝 Sample Analysis:")
    print(f"  Text: {test_text[:80]}...")
    print(f"  Sentiment: {result['sentiment']} {result['emoji']}")
    print(f"  Polarity: {result['polarity']}")
    print(f"  Confidence: {result['confidence']}")
    print(f"  Keywords Found: {result['total_keywords']}")
    
    # Test source comparison
    print(f"\n🔍 Testing Source Comparison...")
    comparison = analyzer.compare_sources_sentiment("BTC")
    
    if comparison:
        print(f"  Market Sentiment: {comparison['market_sentiment']}")
        print(f"  Overall Polarity: {comparison['overall_polarity']}")
        print(f"  Sources Analyzed: {comparison['sources_analyzed']}")
        
        for source, analysis in comparison['source_analysis'].items():
            print(f"    {source.upper()}: {analysis['overall_sentiment']} (polarity: {analysis['average_polarity']})")
    
    return analyzer

if __name__ == "__main__":
    test_advanced_sentiment()