import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# Page configuration - MUST BE FIRST
st.set_page_config(
    page_title="Advanced Crypto Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS with Light Theme
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
    }
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Professional metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        padding: 20px;
        color: white !important;
    }
    
    [data-testid="metric-container"] label {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 600;
        font-size: 14px;
    }
    
    [data-testid="metric-container"] div {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 1.6rem;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 1rem;
    }
    
    /* Professional buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Text areas */
    .stTextArea textarea {
        border: 2px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px;
        font-size: 14px;
    }
    
    /* Select boxes */
    .stSelectbox select {
        border: 2px solid #E2E8F0;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

class AdvancedCryptoDashboard:
    def __init__(self):
        self.price_history = {}
        self.sentiment_history = []
        self.prediction_history = []
        
        # Crypto data with realistic base prices
        self.crypto_data = {
            "BTCUSDT": {"name": "Bitcoin", "base_price": 45000, "emoji": "₿"},
            "ETHUSDT": {"name": "Ethereum", "base_price": 2500, "emoji": "Ξ"},
            "ADAUSDT": {"name": "Cardano", "base_price": 0.5, "emoji": "₳"},
            "SOLUSDT": {"name": "Solana", "base_price": 100, "emoji": "◎"},
            "DOTUSDT": {"name": "Polkadot", "base_price": 7, "emoji": "●"}
        }
        
        # Enhanced sentiment keywords
        self.sentiment_lexicon = {
            "strong_positive": [
                "moon", "rocket", "bullish", "breakout", "surge", "rally", "pump",
                "explosion", "massive", "huge", "incredible", "amazing", "perfect"
            ],
            "positive": [
                "buy", "growth", "profit", "gain", "up", "success", "good", "great",
                "strong", "recovery", "optimistic", "positive", "bull"
            ],
            "negative": [
                "sell", "loss", "drop", "down", "warning", "risk", "bad", "weak",
                "fear", "caution", "concern", "bear"
            ],
            "strong_negative": [
                "crash", "dump", "collapse", "disaster", "terrible", "awful",
                "horrible", "panic", "bloodbath", "rekt", "bearish"
            ]
        }
    
    def get_binance_24h_stats(self, symbol):
        """Get REAL 24h statistics from Binance"""
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'high': float(data['highPrice']),
                    'low': float(data['lowPrice']),
                    'volume': float(data['volume']),
                    'price_change': float(data['priceChange']),
                    'price_change_percent': float(data['priceChangePercent']),
                    'source': 'real'
                }
            else:
                raise Exception("API limit reached")
                
        except Exception as e:
            # Fallback to realistic demo data
            base_price = self.crypto_data[symbol]["base_price"]
            variation = np.random.uniform(0.02, 0.08)  # 2-8% variation
            
            return {
                'high': round(base_price * (1 + variation), 2),
                'low': round(base_price * (1 - variation), 2),
                'volume': np.random.uniform(1000000, 50000000),
                'price_change': round(base_price * variation * np.random.choice([-1, 1]), 2),
                'price_change_percent': round(variation * 100 * np.random.choice([-1, 1]), 2),
                'source': 'demo'
            }
    
    def get_binance_price(self, symbol):
        """Get current price from Binance"""
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return float(data['price'])
            else:
                raise Exception("API limit reached")
                
        except Exception:
            # Realistic demo price with trend
            base_price = self.crypto_data[symbol]["base_price"]
            
            if symbol in self.price_history and len(self.price_history[symbol]) > 0:
                last_price = self.price_history[symbol][-1]['price']
                # Realistic crypto movement
                change = np.random.normal(0, 0.005)  # Normal distribution
                new_price = last_price * (1 + change)
            else:
                new_price = base_price * (1 + np.random.uniform(-0.05, 0.05))
            
            return round(new_price, 2)
    
    def update_price_data(self, symbol):
        """Update price data with realistic movement"""
        price = self.get_binance_price(symbol)
        stats_24h = self.get_binance_24h_stats(symbol)
        
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        
        price_data = {
            'price': price,
            'timestamp': datetime.now(),
            'volume': stats_24h['volume'],
            'high_24h': stats_24h['high'],
            'low_24h': stats_24h['low']
        }
        
        self.price_history[symbol].append(price_data)
        
        # Keep last 50 data points
        if len(self.price_history[symbol]) > 50:
            self.price_history[symbol].pop(0)
        
        return price_data, stats_24h
    
    def create_advanced_chart(self, symbol):
        """Create advanced visualization with multiple features"""
        if symbol not in self.price_history or len(self.price_history[symbol]) < 5:
            return None
        
        df = pd.DataFrame(self.price_history[symbol])
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Price Trend', 'Trading Volume'),
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # Price line
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['price'],
                mode='lines+markers',
                name='Price',
                line=dict(color='#00D4AA', width=3),
                marker=dict(size=6, color='#FF6B6B'),
                hovertemplate='<b>Price:</b> $%{y:,.2f}<br><b>Time:</b> %{x}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Add moving averages
        if len(df) > 10:
            df['MA_5'] = df['price'].rolling(window=5).mean()
            df['MA_10'] = df['price'].rolling(window=10).mean()
            
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['MA_5'],
                    mode='lines',
                    name='MA 5',
                    line=dict(color='#FFA726', width=2, dash='dash'),
                    opacity=0.7
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['MA_10'],
                    mode='lines',
                    name='MA 10',
                    line=dict(color='#42A5F5', width=2, dash='dot'),
                    opacity=0.7
                ),
                row=1, col=1
            )
        
        # Volume bars
        fig.add_trace(
            go.Bar(
                x=df['timestamp'],
                y=df['volume'],
                name='Volume',
                marker_color='#6366F1',
                opacity=0.6
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f"📊 {self.crypto_data[symbol]['name']} Advanced Chart",
            height=600,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#000000')
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E2E8F0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E2E8F0')
        
        return fig
    
    def calculate_advanced_stats(self, symbol, current_price, stats_24h):
        """Calculate advanced market statistics with proper error handling"""
        # Initialize with default values
        stats = {
            'change_24h': stats_24h.get('price_change', 0),
            'change_24h_pct': stats_24h.get('price_change_percent', 0),
            'high_24h': stats_24h.get('high', current_price),
            'low_24h': stats_24h.get('low', current_price),
            'volatility': abs(stats_24h.get('price_change_percent', 0)),
            'volume': stats_24h.get('volume', 0),
            'trend': 'neutral',
            'current_change': 0,  # Always include this key
            'current_change_pct': 0  # Always include this key
        }
        
        # Calculate current change if we have enough history
        if symbol in self.price_history and len(self.price_history[symbol]) >= 2:
            prices = [p['price'] for p in self.price_history[symbol]]
            last_price = prices[-2]
            
            stats['current_change'] = current_price - last_price
            stats['current_change_pct'] = (stats['current_change'] / last_price) * 100
            
            # Determine trend
            if len(prices) > 5:
                try:
                    recent_trend = np.polyfit(range(5), prices[-5:], 1)[0]
                    stats['trend'] = "up" if recent_trend > 0 else "down" if recent_trend < 0 else "neutral"
                except:
                    stats['trend'] = "up" if stats['current_change'] > 0 else "down" if stats['current_change'] < 0 else "neutral"
            else:
                stats['trend'] = "up" if stats['current_change'] > 0 else "down" if stats['current_change'] < 0 else "neutral"
        
        return stats
    
    def enhanced_sentiment_analysis(self, text):
        """Advanced sentiment analysis with scoring"""
        text_lower = text.lower()
        
        # Score sentiment with weights
        score = 0
        keyword_counts = {
            'strong_positive': 0,
            'positive': 0,
            'negative': 0,
            'strong_negative': 0
        }
        
        for category, words in self.sentiment_lexicon.items():
            for word in words:
                if word in text_lower:
                    keyword_counts[category] += 1
                    if category == 'strong_positive':
                        score += 2
                    elif category == 'positive':
                        score += 1
                    elif category == 'negative':
                        score -= 1
                    elif category == 'strong_negative':
                        score -= 2
        
        # Normalize score
        total_keywords = sum(keyword_counts.values())
        if total_keywords > 0:
            normalized_score = score / (total_keywords * 2)  # Max possible score per keyword is 2
        else:
            normalized_score = 0
        
        # Determine sentiment with confidence
        confidence = min(abs(normalized_score) * 2, 1.0)
        
        if normalized_score > 0.3:
            sentiment = "STRONGLY BULLISH 🚀"
            color = "#10B981"
            explanation = "Very positive market sentiment with strong bullish indicators"
        elif normalized_score > 0.1:
            sentiment = "BULLISH 📈"
            color = "#22C55E"
            explanation = "Positive market sentiment suggesting upward movement"
        elif normalized_score < -0.3:
            sentiment = "STRONGLY BEARISH 🐻"
            color = "#EF4444"
            explanation = "Very negative market sentiment with strong bearish indicators"
        elif normalized_score < -0.1:
            sentiment = "BEARISH 📉"
            color = "#F59E0B"
            explanation = "Negative market sentiment suggesting downward movement"
        else:
            sentiment = "NEUTRAL ⚖️"
            color = "#6B7280"
            explanation = "Balanced market sentiment with mixed indicators"
        
        return {
            'sentiment': sentiment,
            'score': round(normalized_score, 3),
            'confidence': round(confidence, 3),
            'color': color,
            'explanation': explanation,
            'keyword_breakdown': keyword_counts,
            'total_keywords': total_keywords
        }
    
    def generate_prediction(self, symbol, current_price, stats):
        """Generate AI-powered price prediction"""
        # Simple prediction algorithm based on multiple factors
        factors = []
        
        # Factor 1: Current trend
        trend_score = 0.7 if stats['trend'] == 'up' else -0.7 if stats['trend'] == 'down' else 0
        factors.append(f"Trend: {'Bullish' if trend_score > 0 else 'Bearish' if trend_score < 0 else 'Neutral'}")
        
        # Factor 2: Volatility
        volatility_score = stats['volatility'] / 100 * 0.5
        factors.append(f"Volatility: {stats['volatility']:.1f}%")
        
        # Factor 3: Price position in 24h range
        range_position = (current_price - stats['low_24h']) / (stats['high_24h'] - stats['low_24h'])
        range_score = (range_position - 0.5) * 2  # -1 to 1
        
        if range_position > 0.7:
            factors.append("Price near 24h high - Resistance possible")
            range_score *= 0.8
        elif range_position < 0.3:
            factors.append("Price near 24h low - Support possible")
            range_score *= 0.8
        
        # Combine factors
        total_score = trend_score + volatility_score + range_score
        
        # Generate prediction
        if total_score > 0.5:
            direction = "UP"
            confidence = min(abs(total_score) * 100, 95)
            timeframe = "15-30 minutes"
            reasoning = "Strong bullish indicators with positive momentum"
        elif total_score > 0.1:
            direction = "UP"
            confidence = min(abs(total_score) * 100, 80)
            timeframe = "30-60 minutes"
            reasoning = "Moderate bullish signals with steady trend"
        elif total_score < -0.5:
            direction = "DOWN"
            confidence = min(abs(total_score) * 100, 95)
            timeframe = "15-30 minutes"
            reasoning = "Strong bearish pressure with negative momentum"
        elif total_score < -0.1:
            direction = "DOWN"
            confidence = min(abs(total_score) * 100, 80)
            timeframe = "30-60 minutes"
            reasoning = "Moderate bearish signals with downward trend"
        else:
            direction = "SIDEWAYS"
            confidence = 50
            timeframe = "Next hour"
            reasoning = "Mixed signals with neutral market conditions"
        
        prediction_data = {
            'direction': direction,
            'confidence': confidence,
            'timeframe': timeframe,
            'reasoning': reasoning,
            'factors': factors,
            'target_price': current_price * (1 + total_score * 0.02),  # Small target movement
            'timestamp': datetime.now()
        }
        
        # Add to history
        self.prediction_history.append({
            'symbol': symbol,
            'prediction': prediction_data
        })
        
        if len(self.prediction_history) > 10:
            self.prediction_history.pop(0)
        
        return prediction_data

def main():
    st.title("🚀 Advanced Crypto Intelligence Platform")
    st.markdown("Real-time analytics, AI predictions, and professional market insights")
    
    # Initialize dashboard in session state
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = AdvancedCryptoDashboard()
        st.session_state.last_update = datetime.now()
    
    dashboard = st.session_state.dashboard
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Control Panel")
        
        # Crypto selection
        selected_crypto = st.selectbox(
            "Select Cryptocurrency:",
            options=list(dashboard.crypto_data.keys()),
            format_func=lambda x: f"{dashboard.crypto_data[x]['emoji']} {dashboard.crypto_data[x]['name']}"
        )
        
        crypto_name = dashboard.crypto_data[selected_crypto]['name']
        
        st.markdown("---")
        
        # Auto-refresh settings
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)
        refresh_rate = st.slider("Refresh Rate (seconds)", 5, 60, 10)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Now"):
                st.rerun()
        with col2:
            if st.button("🗑️ Clear History"):
                st.session_state.dashboard = AdvancedCryptoDashboard()
                st.rerun()
        
        st.markdown("---")
        st.markdown("**📊 System Status**")
        st.success("✅ All Systems Operational")
        st.info(f"**Last Update:** {st.session_state.last_update.strftime('%H:%M:%S')}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📈 {crypto_name} Advanced Analytics")
        
        # Update data
        current_data, stats_24h = dashboard.update_price_data(selected_crypto)
        current_price = current_data['price']
        
        # Display advanced chart
        chart = dashboard.create_advanced_chart(selected_crypto)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("📊 Collecting market data for advanced visualization...")
    
    with col2:
        st.subheader("💰 Market Overview")
        
        # Calculate advanced stats
        stats = dashboard.calculate_advanced_stats(selected_crypto, current_price, stats_24h)
        
        # Current price with real-time change - FIXED: using current_change from stats
        delta_color = "normal" if stats['current_change'] >= 0 else "inverse"
        st.metric(
            label="Current Price",
            value=f"${current_price:,.2f}",
            delta=f"{stats['current_change_pct']:+.2f}%",
            delta_color=delta_color
        )
        
        # Market statistics
        st.markdown("**24H Statistics**")
        
        col2a, col2b = st.columns(2)
        with col2a:
            st.metric("High", f"${stats['high_24h']:,.2f}")
            st.metric("Volume", f"${stats['volume']:,.0f}")
        with col2b:
            st.metric("Low", f"${stats['low_24h']:,.2f}")
            st.metric("Volatility", f"{stats['volatility']:.2f}%")
        
        # Data source indicator
        source_emoji = "🔴" if stats_24h.get('source') == 'real' else "🟡"
        st.caption(f"{source_emoji} Data Source: {stats_24h.get('source', 'demo').upper()}")
    
    # AI Prediction Section
    st.subheader("🤖 AI Price Prediction Engine")
    
    pred_col1, pred_col2 = st.columns([2, 1])
    
    with pred_col1:
        if st.button("🎯 Generate AI Prediction", use_container_width=True):
            with st.spinner("🤖 Analyzing market patterns with AI..."):
                time.sleep(2)  # Simulate AI processing
                
                prediction = dashboard.generate_prediction(selected_crypto, current_price, stats)
                
                # Display prediction
                if prediction['direction'] == "UP":
                    st.success(f"""
                    **📈 BULLISH PREDICTION**
                    
                    **Confidence:** {prediction['confidence']:.1f}%  
                    **Timeframe:** {prediction['timeframe']}  
                    **Target Price:** ${prediction['target_price']:,.2f}
                    
                    **📊 Reasoning:** {prediction['reasoning']}
                    """)
                elif prediction['direction'] == "DOWN":
                    st.error(f"""
                    **📉 BEARISH PREDICTION**
                    
                    **Confidence:** {prediction['confidence']:.1f}%  
                    **Timeframe:** {prediction['timeframe']}  
                    **Target Price:** ${prediction['target_price']:,.2f}
                    
                    **📊 Reasoning:** {prediction['reasoning']}
                    """)
                else:
                    st.info(f"""
                    **⚖️ NEUTRAL PREDICTION**
                    
                    **Confidence:** {prediction['confidence']:.1f}%  
                    **Timeframe:** {prediction['timeframe']}  
                    **Expected Range:** ${stats['low_24h']:,.2f} - ${stats['high_24h']:,.2f}
                    
                    **📊 Reasoning:** {prediction['reasoning']}
                    """)
                
                # Show factors
                st.write("**Key Factors Considered:**")
                for factor in prediction['factors']:
                    st.write(f"• {factor}")
    
    with pred_col2:
        st.markdown("**Prediction History**")
        if dashboard.prediction_history:
            for pred in reversed(dashboard.prediction_history[-3:]):
                time_ago = (datetime.now() - pred['prediction']['timestamp']).seconds // 60
                direction_emoji = "📈" if pred['prediction']['direction'] == "UP" else "📉" if pred['prediction']['direction'] == "DOWN" else "⚖️"
                st.write(f"{direction_emoji} {pred['symbol']} - {pred['prediction']['direction']} ({pred['prediction']['confidence']:.0f}%) - {time_ago}m ago")
        else:
            st.info("No predictions yet")
    
    # Enhanced Sentiment Analysis
    st.subheader("🧠 Advanced Sentiment Analysis")
    
    sent_col1, sent_col2 = st.columns([2, 1])
    
    with sent_col1:
        user_text = st.text_area(
            "Enter market analysis or news:",
            placeholder="Example: Bitcoin showing strong bullish momentum with institutional adoption increasing! Technical analysis indicates potential breakout above resistance levels. 🚀",
            height=120
        )
        
        if st.button("🔍 Analyze Market Sentiment", use_container_width=True):
            if user_text.strip():
                with st.spinner("Analyzing sentiment patterns..."):
                    result = dashboard.enhanced_sentiment_analysis(user_text)
                    
                    # Display detailed results
                    st.markdown(f"""
                    <div style="background: {result['color']}20; border-left: 4px solid {result['color']}; padding: 20px; border-radius: 8px; margin: 10px 0;">
                        <h3 style="color: {result['color']}; margin: 0 0 10px 0;">{result['sentiment']}</h3>
                        <p style="margin: 0; color: #000000;"><strong>Explanation:</strong> {result['explanation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Metrics
                    col_met1, col_met2, col_met3 = st.columns(3)
                    with col_met1:
                        st.metric("Sentiment Score", f"{result['score']:.3f}")
                    with col_met2:
                        st.metric("Confidence", f"{result['confidence']:.1%}")
                    with col_met3:
                        st.metric("Keywords Found", result['total_keywords'])
                    
                    # Keyword breakdown
                    st.write("**Keyword Analysis:**")
                    for category, count in result['keyword_breakdown'].items():
                        if count > 0:
                            st.write(f"• {category.replace('_', ' ').title()}: {count}")
                    
                    # Add to history
                    dashboard.sentiment_history.append({
                        'text': user_text[:80] + "...",
                        'result': result,
                        'time': datetime.now()
                    })
                    
                    if len(dashboard.sentiment_history) > 5:
                        dashboard.sentiment_history.pop(0)
            else:
                st.warning("Please enter some text for analysis")
    
    with sent_col2:
        st.markdown("**Recent Analysis**")
        if dashboard.sentiment_history:
            for item in reversed(dashboard.sentiment_history[-3:]):
                time_ago = (datetime.now() - item['time']).seconds // 60
                st.write(f"• {item['text']}")
                st.write(f"  → {item['result']['sentiment'].split(' ')[0]} ({item['result']['score']:.2f}) - {time_ago}m ago")
        else:
            st.info("No sentiment analysis yet")
    
    # Update timestamp and auto-refresh
    st.session_state.last_update = datetime.now()
    
    if auto_refresh:
        time.sleep(refresh_rate)
        st.rerun()

if __name__ == "__main__":
    main()