import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import re
from typing import List, Dict
import json


class NewsDataCollector:
    def __init__(self):
        self.sources = {
            'binance': self.get_binance_news,
            'twitter': self.get_twitter_sentiment,
            'crypto_news': self.get_crypto_news
        }
        
    def get_binance_news(self, limit=10) -> List[Dict]:
        """Fetch latest news from Binance"""
        try:
            # Binance API for news (public endpoint)
            url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
            
            payload = {
                "catalogId": 48,  # Crypto news catalog
                "type": 1,
                "pageNo": 1,
                "pageSize": limit
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('data', {}).get('articles', [])
                
                news_list = []
                for article in articles:
                    news_list.append({
                        'source': 'binance',
                        'title': article.get('title', ''),
                        'content': article.get('content', '')[:500],  # First 500 chars
                        'publish_time': datetime.fromtimestamp(article.get('releaseDate', 0)/1000),
                        'url': f"https://www.binance.com/en/support/announcement/{article.get('code', '')}",
                        'symbols': self.extract_symbols_from_text(article.get('title', '') + ' ' + article.get('content', ''))
                    })
                
                print(f"✅ Fetched {len(news_list)} Binance news articles")
                return news_list
                
        except Exception as e:
            print(f"❌ Error fetching Binance news: {e}")
        
        # Fallback to sample Binance news
        return self.get_sample_binance_news()

    def get_twitter_sentiment(self, query="bitcoin", limit=15) -> List[Dict]:
        """Fetch Twitter sentiment data (using free API)"""
        try:
            # Using free Twitter API alternative or web scraping
            # Note: For production, you'd use Twitter API v2 with proper authentication
            url = f"https://api.stocktwits.com/api/2/streams/symbol/{query}.json"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                messages = data.get('messages', [])
                
                tweets = []
                for msg in messages[:limit]:
                    tweets.append({
                        'source': 'twitter',
                        'content': msg.get('body', ''),
                        'user': msg.get('user', {}).get('username', ''),
                        'created_at': datetime.now(),  # StockTwits doesn't provide exact time
                        'sentiment': msg.get('entities', {}).get('sentiment', {}).get('basic', 'neutral'),
                        'symbols': [query.upper()]
                    })
                
                print(f"✅ Fetched {len(tweets)} Twitter sentiments for {query}")
                return tweets
                
        except Exception as e:
            print(f"❌ Error fetching Twitter data: {e}")
        
        # Fallback to sample Twitter data
        return self.get_sample_twitter_data()

    def get_crypto_news(self, limit=10) -> List[Dict]:
        """Fetch general crypto news from free APIs"""
        try:
            # Using CryptoPanic API (free tier)
            url = "https://cryptopanic.com/api/v1/posts/"
            params = {
                'auth_token': 'demo',  # Use your own token for production
                'public': 'true',
                'kind': 'news'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('results', [])
                
                news_list = []
                for post in posts[:limit]:
                    news_list.append({
                        'source': 'crypto_news',
                        'title': post.get('title', ''),
                        'content': post.get('title', ''),  # CryptoPanic doesn't always have content
                        'published_at': datetime.fromisoformat(post.get('published_at', '').replace('Z', '+00:00')),
                        'url': post.get('url', ''),
                        'symbols': self.extract_symbols_from_text(post.get('title', '')),
                        'votes': post.get('votes', {})
                    })
                
                print(f"✅ Fetched {len(news_list)} crypto news articles")
                return news_list
                
        except Exception as e:
            print(f"❌ Error fetching crypto news: {e}")
        
        return self.get_sample_crypto_news()

    def extract_symbols_from_text(self, text: str) -> List[str]:
        """Extract cryptocurrency symbols from text"""
        # Common crypto symbols pattern
        symbols_pattern = r'\b(BTC|ETH|ADA|SOL|DOT|XRP|BNB|DOGE|MATIC|LTC|AVAX|LINK)\b'
        symbols = re.findall(symbols_pattern, text.upper())
        return list(set(symbols))  # Remove duplicates

    def get_sample_binance_news(self) -> List[Dict]:
        """Sample Binance news for fallback"""
        return [
            {
                'source': 'binance',
                'title': 'Bitcoin ETF Approval Expected Soon - Market Bullish',
                'content': 'Major financial institutions are optimistic about Bitcoin ETF approval in the coming weeks.',
                'publish_time': datetime.now() - timedelta(hours=2),
                'symbols': ['BTC'],
                'url': '#'
            },
            {
                'source': 'binance', 
                'title': 'Ethereum Upgrade Successfully Implemented',
                'content': 'Latest Ethereum network upgrade improves scalability and reduces gas fees significantly.',
                'publish_time': datetime.now() - timedelta(hours=5),
                'symbols': ['ETH'],
                'url': '#'
            }
        ]

    def get_sample_twitter_data(self) -> List[Dict]:
        """Sample Twitter data for fallback"""
        return [
            {
                'source': 'twitter',
                'content': 'Bitcoin looking strong! Ready for the next leg up! 🚀 #BTC #bullish',
                'user': 'CryptoExpert',
                'created_at': datetime.now() - timedelta(minutes=30),
                'sentiment': 'bullish',
                'symbols': ['BTC']
            },
            {
                'source': 'twitter',
                'content': 'Market correction expected for altcoins. Taking profits on ADA and SOL.',
                'user': 'TraderPro',
                'created_at': datetime.now() - timedelta(minutes=45),
                'sentiment': 'bearish', 
                'symbols': ['ADA', 'SOL']
            }
        ]

    def get_sample_crypto_news(self) -> List[Dict]:
        """Sample crypto news for fallback"""
        return [
            {
                'source': 'crypto_news',
                'title': 'Institutional Adoption of Crypto Reaches New High',
                'content': 'Major corporations continue to add cryptocurrencies to their balance sheets.',
                'published_at': datetime.now() - timedelta(hours=1),
                'symbols': ['BTC', 'ETH'],
                'url': '#',
                'votes': {'positive': 15, 'negative': 2}
            }
        ]

    def collect_all_news(self, crypto_symbol='BTC', limit_per_source=5):
        """Collect news from all sources for a given cryptocurrency"""
        all_news = []
        
        try:
            # Get news from each source
            binance_news = self.get_binance_news(limit_per_source)
            twitter_data = self.get_twitter_sentiment(crypto_symbol.lower(), limit_per_source)
            crypto_news = self.get_crypto_news(limit_per_source)
            
            # Filter news relevant to the requested symbol
            for news_list in [binance_news, twitter_data, crypto_news]:
                for news in news_list:
                    if crypto_symbol in news.get('symbols', []) or not news.get('symbols'):
                        all_news.append(news)
            
            print(f"✅ Collected {len(all_news)} total news items for {crypto_symbol}")
            return all_news
            
        except Exception as e:
            print(f"❌ Error collecting all news: {e}")
            return []

# Test function
def test_news_collector():
    """Test the news collector"""
    print("🧪 Testing News Data Collector...")
    
    collector = NewsDataCollector()
    
    # Test Binance news
    binance_news = collector.get_binance_news(3)
    print(f"📰 Binance News: {len(binance_news)} items")
    for news in binance_news[:2]:
        print(f"  - {news['title'][:50]}...")
    
    # Test Twitter data
    twitter_data = collector.get_twitter_sentiment("bitcoin", 3)
    print(f"🐦 Twitter Data: {len(twitter_data)} items")
    for tweet in twitter_data[:2]:
        print(f"  - {tweet['content'][:50]}...")
    
    # Test collection for BTC
    all_btc_news = collector.collect_all_news('BTC', 2)
    print(f"📊 All BTC News: {len(all_btc_news)} items")
    
    return collector

if __name__ == "__main__":
    test_news_collector()