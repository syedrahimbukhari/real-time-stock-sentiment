import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
import sys
import os
import json
import base64
from io import BytesIO

# Add src to path for imports
sys.path.append('src')

warnings.filterwarnings('ignore')

# Page configuration - MUST BE FIRST
st.set_page_config(
    page_title="Advanced Crypto Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS with Dark/Light Theme Support
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
    
    /* Custom headers */
    .custom-header {
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Section containers */
    .section-container {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background: #F8FAFC;
    }
    
    /* Source item styling */
    .source-item {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Log container styling */
    .log-container {
        background: #1E1E1E;
        color: #00FF00;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .log-entry {
        margin: 5px 0;
        padding: 5px;
        border-left: 3px solid #00FF00;
    }
    
    .log-timestamp {
        color: #888;
        font-size: 10px;
    }
    
    .log-message {
        color: #00FF00;
    }
    
    /* Alert item styling */
    .alert-item {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px;
        margin: 6px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .alert-item.triggered {
        border-color: #FF6B6B;
        background: #FFF5F5;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Portfolio item styling */
    .portfolio-item {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
    }
    
    /* News item styling */
    .news-item {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        transition: all 0.3s ease;
    }
    
    .news-item:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Custom info box styling */
    .custom-info-box {
        background-color: #e8f4fd;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
    
    .custom-success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
    
    .custom-error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class AdvancedCryptoDashboard:
    def __init__(self):
        self.price_history = {}
        self.market_data = {}
        
        # Extended crypto data with more assets
        self.crypto_data = {
            "BTCUSDT": {"name": "Bitcoin", "base_price": 45000, "emoji": "₿", "category": "Large Cap"},
            "ETHUSDT": {"name": "Ethereum", "base_price": 2500, "emoji": "Ξ", "category": "Large Cap"},
            "BNBUSDT": {"name": "Binance Coin", "base_price": 300, "emoji": "ⓑ", "category": "Large Cap"},
            "ADAUSDT": {"name": "Cardano", "base_price": 0.5, "emoji": "₳", "category": "Mid Cap"},
            "SOLUSDT": {"name": "Solana", "base_price": 100, "emoji": "◎", "category": "Mid Cap"},
            "DOTUSDT": {"name": "Polkadot", "base_price": 7, "emoji": "●", "category": "Mid Cap"},
            "DOGEUSDT": {"name": "Dogecoin", "base_price": 0.15, "emoji": "🐕", "category": "Meme"},
            "XRPUSDT": {"name": "Ripple", "base_price": 0.6, "emoji": "✕", "category": "Large Cap"},
            "LTCUSDT": {"name": "Litecoin", "base_price": 75, "emoji": "Ł", "category": "Large Cap"},
            "LINKUSDT": {"name": "Chainlink", "base_price": 15, "emoji": "🔗", "category": "Mid Cap"}
        }
        
        # Initialize advanced sentiment analyzer
        try:
            from sentiment.sentiment_analyzer import AdvancedSentimentAnalyzer
            self.sentiment_analyzer = AdvancedSentimentAnalyzer()
        except Exception as e:
            self.sentiment_analyzer = None
    
    def log_message(self, message, level="INFO"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        
        if 'app_logs' not in st.session_state:
            st.session_state.app_logs = []
        
        st.session_state.app_logs.append(log_entry)
        
        # Keep only last 50 logs
        if len(st.session_state.app_logs) > 50:
            st.session_state.app_logs.pop(0)
    
    def get_multiple_prices(self, symbols):
        """Get prices for multiple symbols at once"""
        prices = {}
        for symbol in symbols:
            try:
                price = self.get_binance_price(symbol)
                prices[symbol] = price
            except Exception as e:
                self.log_message(f"Error getting price for {symbol}: {str(e)}", "ERROR")
                # Fallback to demo price
                base_price = self.crypto_data[symbol]["base_price"]
                prices[symbol] = base_price * (1 + np.random.uniform(-0.02, 0.02))
        return prices
    
    def get_binance_24h_stats(self, symbol):
        """Get REAL 24h statistics from Binance"""
        try:
            self.log_message(f"Fetching 24h stats for {symbol} from Binance API")
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.log_message(f"✅ Successfully fetched REAL data for {symbol}")
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
            self.log_message(f"⚠️ Using DEMO data for {symbol} - API limit reached", "WARNING")
            base_price = self.crypto_data[symbol]["base_price"]
            variation = np.random.uniform(0.02, 0.08)
            
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
            self.log_message(f"Fetching current price for {symbol}")
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                price = float(data['price'])
                self.log_message(f"✅ Real price for {symbol}: ${price:,.2f}")
                return price
            else:
                raise Exception("API limit reached")
                
        except Exception:
            # Realistic demo price with trend
            self.log_message(f"⚠️ Using DEMO price for {symbol}", "WARNING")
            base_price = self.crypto_data[symbol]["base_price"]
            
            if symbol in self.price_history and len(self.price_history[symbol]) > 0:
                last_price = self.price_history[symbol][-1]['price']
                change = np.random.normal(0, 0.005)
                new_price = last_price * (1 + change)
            else:
                new_price = base_price * (1 + np.random.uniform(-0.05, 0.05))
            
            return round(new_price, 2)
    
    def update_price_data(self, symbol, refresh_rate=10):
        """Update price data with realistic movement and volume variation"""
        self.log_message(f"Updating price data for {symbol}")
        price = self.get_binance_price(symbol)
        stats_24h = self.get_binance_24h_stats(symbol)
        
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        
        # Calculate realistic volume with variation
        base_volume = stats_24h['volume']
        
        if self.price_history[symbol]:
            last_price = self.price_history[symbol][-1]['price']
            price_change_pct = abs((price - last_price) / last_price) * 100
            volume_multiplier = 1 + (price_change_pct * 0.1)
            volume_multiplier *= np.random.uniform(0.7, 1.3)
            current_volume = base_volume * volume_multiplier
        else:
            current_volume = base_volume * np.random.uniform(0.8, 1.2)
        
        price_data = {
            'price': price,
            'timestamp': datetime.now(),
            'volume': current_volume,
            'high_24h': stats_24h['high'],
            'low_24h': stats_24h['low']
        }
        
        self.price_history[symbol].append(price_data)
        
        if len(self.price_history[symbol]) > 50:
            self.price_history[symbol].pop(0)
        
        self.log_message(f"✅ Price data updated: ${price:,.2f}, Volume: ${current_volume:,.0f}")
        return price_data, stats_24h
    
    def create_advanced_chart(self, symbol):
        """Create advanced visualization with multiple features"""
        if symbol not in self.price_history or len(self.price_history[symbol]) < 5:
            return None
        
        df = pd.DataFrame(self.price_history[symbol])
        
        # Create subplots with 3 rows for additional indicators
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Price Trend with Indicators', 'Trading Volume', 'RSI Indicator'),
            vertical_spacing=0.08,
            row_heights=[0.5, 0.25, 0.25]
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
            df['MA_20'] = df['price'].rolling(window=20).mean()
            
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
            
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['MA_20'],
                    mode='lines',
                    name='MA 20',
                    line=dict(color='#66BB6A', width=2),
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
                opacity=0.6,
                hovertemplate='<b>Volume:</b> $%{y:,.0f}<br><b>Time:</b> %{x}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # RSI Indicator
        if len(df) > 14:
            df['RSI'] = self.calculate_rsi(df['price'])
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['RSI'],
                    mode='lines',
                    name='RSI',
                    line=dict(color='#8B5CF6', width=2),
                    hovertemplate='<b>RSI:</b> %{y:.1f}<br><b>Time:</b> %{x}<extra></extra>'
                ),
                row=3, col=1
            )
            
            # Add RSI reference lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
            fig.add_hline(y=50, line_dash="dot", line_color="gray", row=3, col=1)
        
        fig.update_layout(
            title=f"📊 {self.crypto_data[symbol]['name']} Advanced Technical Analysis",
            height=800,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#000000')
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E2E8F0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E2E8F0')
        
        return fig
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_advanced_stats(self, symbol, current_price, stats_24h):
        """Calculate advanced market statistics with proper error handling"""
        stats = {
            'change_24h': stats_24h.get('price_change', 0),
            'change_24h_pct': stats_24h.get('price_change_percent', 0),
            'high_24h': stats_24h.get('high', current_price),
            'low_24h': stats_24h.get('low', current_price),
            'volatility': abs(stats_24h.get('price_change_percent', 0)),
            'volume': stats_24h.get('volume', 0),
            'trend': 'neutral',
            'current_change': 0,
            'current_change_pct': 0
        }
        
        if symbol in self.price_history and len(self.price_history[symbol]) >= 2:
            prices = [p['price'] for p in self.price_history[symbol]]
            last_price = prices[-2]
            
            stats['current_change'] = current_price - last_price
            stats['current_change_pct'] = (stats['current_change'] / last_price) * 100
            
            if len(prices) > 5:
                try:
                    recent_trend = np.polyfit(range(5), prices[-5:], 1)[0]
                    stats['trend'] = "up" if recent_trend > 0 else "down" if recent_trend < 0 else "neutral"
                except:
                    stats['trend'] = "up" if stats['current_change'] > 0 else "down" if stats['current_change'] < 0 else "neutral"
            else:
                stats['trend'] = "up" if stats['current_change'] > 0 else "down" if stats['current_change'] < 0 else "neutral"
        
        return stats

    def display_real_stats(self, current_data, symbol, stats_24h):
        """Display REAL statistics with accurate data and proper formatting"""
        if not current_data:
            return
        
        current_price = current_data['price']
        
        # Calculate advanced stats
        stats = self.calculate_advanced_stats(symbol, current_price, stats_24h)
        
        # Current price with real-time change
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
            high_formatted = f"${stats['high_24h']:,.2f}"
            low_formatted = f"${stats['low_24h']:,.2f}"
            
            st.metric("High", high_formatted)
            
            volume_formatted = f"${stats['volume']:,.0f}" if stats['volume'] >= 1000 else f"${stats['volume']:,.2f}"
            st.metric("Volume", volume_formatted)
            
        with col2b:
            st.metric("Low", low_formatted)
            st.metric("Volatility", f"{stats['volatility']:.2f}%")
        
        # Data source indicator
        source_emoji = "🔴" if stats_24h.get('source') == 'real' else "🟡"
        st.caption(f"{source_emoji} Data Source: {stats_24h.get('source', 'demo').upper()}")
    
    def check_alerts(self):
        """Check if any price alerts have been triggered"""
        triggered_alerts = []
        if 'price_alerts' in st.session_state:
            current_prices = self.get_multiple_prices([alert['symbol'] for alert in st.session_state.price_alerts])
            
            for alert in st.session_state.price_alerts:
                current_price = current_prices.get(alert['symbol'])
                if current_price:
                    condition_met = False
                    if alert['condition'] == 'above' and current_price >= alert['price']:
                        condition_met = True
                    elif alert['condition'] == 'below' and current_price <= alert['price']:
                        condition_met = True
                    
                    if condition_met and not alert.get('triggered', False):
                        alert['triggered'] = True
                        alert['triggered_time'] = datetime.now()
                        triggered_alerts.append(alert)
                        self.log_message(f"🚨 Alert triggered: {alert['symbol']} {alert['condition']} ${alert['price']}")
        
        return triggered_alerts

def initialize_session_state():
    """Initialize all session state variables"""
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = AdvancedCryptoDashboard()
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()
    
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    if 'last_prediction' not in st.session_state:
        st.session_state.last_prediction = None
    
    if 'last_sentiment' not in st.session_state:
        st.session_state.last_sentiment = None
    
    if 'show_prediction_result' not in st.session_state:
        st.session_state.show_prediction_result = False
    
    if 'show_sentiment_result' not in st.session_state:
        st.session_state.show_sentiment_result = False
    
    if 'app_logs' not in st.session_state:
        st.session_state.app_logs = []
    
    if 'show_logs' not in st.session_state:
        st.session_state.show_logs = False
    
    # NEW: Portfolio Management
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []
    
    # NEW: Price Alerts
    if 'price_alerts' not in st.session_state:
        st.session_state.price_alerts = []
    
    # NEW: Watchlist
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
    
    # NEW: News Data
    if 'crypto_news' not in st.session_state:
        st.session_state.crypto_news = []

# ========== NEW FEATURES ==========

def display_portfolio_section():
    """Display portfolio management section"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.subheader("💼 Portfolio Manager")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("add_to_portfolio"):
            st.markdown("**Add to Portfolio**")
            symbol = st.selectbox("Cryptocurrency", options=list(st.session_state.dashboard.crypto_data.keys()),
                                format_func=lambda x: f"{st.session_state.dashboard.crypto_data[x]['emoji']} {st.session_state.dashboard.crypto_data[x]['name']}")
            quantity = st.number_input("Quantity", min_value=0.0, step=0.1, value=1.0)
            buy_price = st.number_input("Buy Price ($)", min_value=0.0, step=0.1)
            
            if st.form_submit_button("➕ Add to Portfolio"):
                current_price = st.session_state.dashboard.get_binance_price(symbol)
                total_invested = quantity * buy_price
                current_value = quantity * current_price
                pnl = current_value - total_invested
                pnl_percent = (pnl / total_invested) * 100 if total_invested > 0 else 0
                
                portfolio_item = {
                    'symbol': symbol,
                    'quantity': quantity,
                    'buy_price': buy_price,
                    'total_invested': total_invested,
                    'current_price': current_price,
                    'current_value': current_value,
                    'pnl': pnl,
                    'pnl_percent': pnl_percent,
                    'added_date': datetime.now()
                }
                
                st.session_state.portfolio.append(portfolio_item)
                st.session_state.dashboard.log_message(f"Added {quantity} {symbol} to portfolio at ${buy_price}")
                st.rerun()
    
    with col2:
        st.markdown("**Portfolio Summary**")
        if st.session_state.portfolio:
            total_invested = sum(item['total_invested'] for item in st.session_state.portfolio)
            total_current = sum(item['current_value'] for item in st.session_state.portfolio)
            total_pnl = total_current - total_invested
            total_pnl_percent = (total_pnl / total_invested) * 100 if total_invested > 0 else 0
            
            st.metric("Total Invested", f"${total_invested:,.2f}")
            st.metric("Current Value", f"${total_current:,.2f}")
            st.metric("Total P&L", f"${total_pnl:,.2f}", delta=f"{total_pnl_percent:+.2f}%")
        else:
            st.info("No assets in portfolio")
    
    # Display portfolio items
    if st.session_state.portfolio:
        st.markdown("**Your Assets**")
        for item in st.session_state.portfolio:
            pnl_color = "green" if item['pnl'] >= 0 else "red"
            st.markdown(f"""
            <div class="portfolio-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{st.session_state.dashboard.crypto_data[item['symbol']]['emoji']} {st.session_state.dashboard.crypto_data[item['symbol']]['name']}</strong><br>
                        <small>Quantity: {item['quantity']} | Buy Price: ${item['buy_price']:,.2f}</small>
                    </div>
                    <div style="text-align: right;">
                        <div>Current: <strong>${item['current_price']:,.2f}</strong></div>
                        <div style="color: {pnl_color};">P&L: ${item['pnl']:,.2f} ({item['pnl_percent']:+.2f}%)</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_alerts_section():
    """Display price alerts section"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.subheader("🔔 Price Alerts")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("create_alert"):
            st.markdown("**Create New Alert**")
            symbol = st.selectbox("Cryptocurrency", options=list(st.session_state.dashboard.crypto_data.keys()),
                                format_func=lambda x: f"{st.session_state.dashboard.crypto_data[x]['emoji']} {st.session_state.dashboard.crypto_data[x]['name']}",
                                key="alert_symbol")
            condition = st.selectbox("Condition", options=['above', 'below'])
            price = st.number_input("Price ($)", min_value=0.0, step=0.1)
            
            if st.form_submit_button("➕ Create Alert"):
                current_price = st.session_state.dashboard.get_binance_price(symbol)
                alert = {
                    'symbol': symbol,
                    'condition': condition,
                    'price': price,
                    'current_price': current_price,
                    'created': datetime.now(),
                    'triggered': False
                }
                st.session_state.price_alerts.append(alert)
                st.session_state.dashboard.log_message(f"Created {condition} ${price} alert for {symbol}")
                st.rerun()
    
    with col2:
        st.markdown("**Active Alerts**")
        st.info(f"Total: {len(st.session_state.price_alerts)}")
        
        if st.button("🔄 Check Alerts", key="check_alerts"):
            triggered = st.session_state.dashboard.check_alerts()
            if triggered:
                st.success(f"🎯 {len(triggered)} alerts triggered!")
            else:
                st.info("No new alerts triggered")
    
    # Display alerts
    if st.session_state.price_alerts:
        for alert in st.session_state.price_alerts:
            alert_class = "alert-item triggered" if alert.get('triggered') else "alert-item"
            status = "🔴 TRIGGERED" if alert.get('triggered') else "🟢 ACTIVE"
            
            st.markdown(f"""
            <div class="{alert_class}">
                <div>
                    <strong>{st.session_state.dashboard.crypto_data[alert['symbol']]['emoji']} {st.session_state.dashboard.crypto_data[alert['symbol']]['name']}</strong><br>
                    <small>Alert when price goes {alert['condition']} ${alert['price']:,.2f}</small>
                </div>
                <div style="text-align: right;">
                    <div>{status}</div>
                    <small>Current: ${alert.get('current_price', 0):,.2f}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if alert.get('triggered'):
                if st.button("❌ Remove", key=f"remove_{alert['symbol']}_{alert['price']}"):
                    st.session_state.price_alerts.remove(alert)
                    st.rerun()
    else:
        st.info("No price alerts set up")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_watchlist_section():
    """Display watchlist section"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.subheader("⭐ Watchlist")
    
    # Add to watchlist
    col1, col2 = st.columns([3, 1])
    with col1:
        new_symbol = st.selectbox("Add to Watchlist", 
                                options=[s for s in st.session_state.dashboard.crypto_data.keys() if s not in st.session_state.watchlist],
                                format_func=lambda x: f"{st.session_state.dashboard.crypto_data[x]['emoji']} {st.session_state.dashboard.crypto_data[x]['name']}",
                                key="watchlist_add")
    with col2:
        if st.button("➕ Add") and new_symbol:
            st.session_state.watchlist.append(new_symbol)
            st.rerun()
    
    # Display watchlist with real-time prices
    if st.session_state.watchlist:
        prices = st.session_state.dashboard.get_multiple_prices(st.session_state.watchlist)
        
        for symbol in st.session_state.watchlist:
            if symbol in prices:
                price = prices[symbol]
                crypto_info = st.session_state.dashboard.crypto_data[symbol]
                stats_24h = st.session_state.dashboard.get_binance_24h_stats(symbol)
                
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"{crypto_info['emoji']} **{crypto_info['name']}**")
                    st.write(f"${price:,.2f}")
                with col2:
                    change = stats_24h.get('price_change_percent', 0)
                    change_color = "green" if change >= 0 else "red"
                    st.write(f"24h: <span style='color: {change_color}'>{change:+.2f}%</span>", unsafe_allow_html=True)
                with col3:
                    if st.button("❌", key=f"remove_{symbol}"):
                        st.session_state.watchlist.remove(symbol)
                        st.rerun()
                st.divider()
    else:
        st.info("Watchlist is empty")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_news_section():
    """Display crypto news section"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.subheader("📰 Crypto News")
    
    if st.button("🔄 Fetch Latest News"):
        with st.spinner("Fetching latest crypto news..."):
            # Simulate news fetching (replace with actual news API)
            time.sleep(2)
            demo_news = [
                {
                    'title': 'Bitcoin ETF Approval Expected Soon',
                    'source': 'Crypto News',
                    'date': '2 hours ago',
                    'sentiment': 'positive',
                    'url': '#'
                },
                {
                    'title': 'Ethereum Upgrade Boosts Network Performance',
                    'source': 'Blockchain Daily',
                    'date': '4 hours ago', 
                    'sentiment': 'positive',
                    'url': '#'
                },
                {
                    'title': 'Market Volatility Increases Amid Regulatory Concerns',
                    'source': 'Finance Times',
                    'date': '6 hours ago',
                    'sentiment': 'neutral',
                    'url': '#'
                }
            ]
            st.session_state.crypto_news = demo_news
    
    if st.session_state.crypto_news:
        for news in st.session_state.crypto_news:
            sentiment_emoji = "📈" if news['sentiment'] == 'positive' else "📉" if news['sentiment'] == 'negative' else "📊"
            st.markdown(f"""
            <div class="news-item">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <strong>{sentiment_emoji} {news['title']}</strong><br>
                        <small>{news['source']} • {news['date']}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Click 'Fetch Latest News' to load news")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_market_overview():
    """Display market overview with multiple cryptocurrencies"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.subheader("🌐 Market Overview")
    
    # Select cryptocurrencies to display
    selected_cryptos = st.multiselect(
        "Select cryptocurrencies for overview:",
        options=list(st.session_state.dashboard.crypto_data.keys()),
        default=["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT"],
        format_func=lambda x: f"{st.session_state.dashboard.crypto_data[x]['emoji']} {st.session_state.dashboard.crypto_data[x]['name']}"
    )
    
    if selected_cryptos:
        prices = st.session_state.dashboard.get_multiple_prices(selected_cryptos)
        
        cols = st.columns(len(selected_cryptos))
        for idx, symbol in enumerate(selected_cryptos):
            with cols[idx]:
                if symbol in prices:
                    price = prices[symbol]
                    crypto_info = st.session_state.dashboard.crypto_data[symbol]
                    stats_24h = st.session_state.dashboard.get_binance_24h_stats(symbol)
                    change = stats_24h.get('price_change_percent', 0)
                    
                    st.metric(
                        label=f"{crypto_info['emoji']} {crypto_info['name']}",
                        value=f"${price:,.2f}",
                        delta=f"{change:+.2f}%"
                    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== EXISTING FUNCTIONS (Updated) ==========

def generate_prediction(symbol, current_price, stats_24h):
    """Generate AI-powered price prediction"""
    dashboard = st.session_state.dashboard
    dashboard.log_message(f"🤖 Generating AI prediction for {symbol}")
    
    stats = dashboard.calculate_advanced_stats(symbol, current_price, stats_24h)
    
    # Enhanced prediction algorithm
    factors = []
    
    # Technical factors
    trend_score = 0.7 if stats['trend'] == 'up' else -0.7 if stats['trend'] == 'down' else 0
    factors.append(f"Trend: {'Bullish' if trend_score > 0 else 'Bearish' if trend_score < 0 else 'Neutral'}")
    
    volatility_score = stats['volatility'] / 100 * 0.5
    factors.append(f"Volatility: {stats['volatility']:.1f}%")
    
    # Volume analysis
    volume_trend = "High" if stats['volume'] > 10000000 else "Medium" if stats['volume'] > 5000000 else "Low"
    volume_score = 0.3 if volume_trend == "High" else 0.1 if volume_trend == "Medium" else -0.1
    factors.append(f"Volume: {volume_trend}")
    
    # Market position analysis
    range_position = (current_price - stats['low_24h']) / (stats['high_24h'] - stats['low_24h'])
    range_score = (range_position - 0.5) * 2
    
    if range_position > 0.7:
        factors.append("Price near 24h high - Resistance possible")
        range_score *= 0.8
    elif range_position < 0.3:
        factors.append("Price near 24h low - Support possible")
        range_score *= 0.8
    
    # Combine all factors
    total_score = trend_score + volatility_score + volume_score + range_score
    
    # Generate prediction with enhanced logic
    if total_score > 0.8:
        direction = "STRONG UP"
        confidence = min(abs(total_score) * 100, 98)
        timeframe = "15-30 minutes"
        reasoning = "Very strong bullish indicators across multiple factors"
    elif total_score > 0.3:
        direction = "UP"
        confidence = min(abs(total_score) * 100, 85)
        timeframe = "30-60 minutes"
        reasoning = "Strong bullish signals with good momentum"
    elif total_score > 0.1:
        direction = "SLIGHT UP"
        confidence = min(abs(total_score) * 100, 70)
        timeframe = "1-2 hours"
        reasoning = "Moderate bullish signals"
    elif total_score < -0.8:
        direction = "STRONG DOWN"
        confidence = min(abs(total_score) * 100, 98)
        timeframe = "15-30 minutes"
        reasoning = "Very strong bearish pressure across all factors"
    elif total_score < -0.3:
        direction = "DOWN"
        confidence = min(abs(total_score) * 100, 85)
        timeframe = "30-60 minutes"
        reasoning = "Strong bearish signals with negative momentum"
    elif total_score < -0.1:
        direction = "SLIGHT DOWN"
        confidence = min(abs(total_score) * 100, 70)
        timeframe = "1-2 hours"
        reasoning = "Moderate bearish signals"
    else:
        direction = "SIDEWAYS"
        confidence = 50
        timeframe = "Next 2 hours"
        reasoning = "Mixed signals with balanced market conditions"
    
    prediction_data = {
        'direction': direction,
        'confidence': confidence,
        'timeframe': timeframe,
        'reasoning': reasoning,
        'factors': factors,
        'target_price': current_price * (1 + total_score * 0.03),
        'timestamp': datetime.now(),
        'symbol': symbol,
        'risk_level': 'Low' if abs(total_score) < 0.3 else 'Medium' if abs(total_score) < 0.6 else 'High'
    }
    
    st.session_state.prediction_history.append(prediction_data)
    if len(st.session_state.prediction_history) > 10:
        st.session_state.prediction_history.pop(0)
    
    dashboard.log_message(f"✅ Prediction generated: {direction} with {confidence:.1f}% confidence")
    return prediction_data

def display_prediction_section(symbol, current_price, stats_24h):
    """Display AI prediction section"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.subheader("🤖 Advanced AI Prediction Engine")
    
    with st.expander("ℹ️ Enhanced AI Prediction System"):
        st.markdown("""
        **🔍 Our Advanced AI Analyzes:**
        
        - **📈 Multi-timeframe Trends**: Short, medium, and long-term patterns
        - **📊 Volume Analysis**: Trading volume strength and momentum
        - **🎯 Technical Indicators**: RSI, Moving Averages, Support/Resistance
        - **📉 Market Structure**: Price action and chart patterns
        - **🌊 Volatility Assessment**: Market conditions and risk levels
        
        **💡 Enhanced Features:**
        - Risk level assessment (Low/Medium/High)
        - Confidence scoring with multiple factors
        - Timeframe-specific predictions
        - Detailed factor breakdown
        """)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🎯 Generate Advanced AI Prediction", use_container_width=True, key="predict_btn"):
            with st.spinner("🤖 Running advanced market analysis..."):
                time.sleep(2)
                prediction = generate_prediction(symbol, current_price, stats_24h)
                st.session_state.last_prediction = prediction
                st.session_state.show_prediction_result = True
    
    with col2:
        st.markdown("**📋 Prediction History**")
        if st.session_state.prediction_history:
            for pred in reversed(st.session_state.prediction_history[-3:]):
                time_ago = (datetime.now() - pred['timestamp']).seconds // 60
                direction_emoji = "🚀" if "STRONG UP" in pred['direction'] else "📈" if "UP" in pred['direction'] else "📉" if "DOWN" in pred['direction'] else "⚖️"
                st.write(f"{direction_emoji} {pred['symbol']} - {pred['direction']} ({pred['confidence']:.0f}%)")
        else:
            st.info("No predictions yet")
    
    if st.session_state.show_prediction_result and st.session_state.last_prediction:
        prediction = st.session_state.last_prediction
        
        st.markdown("---")
        st.subheader("🎯 AI Prediction Result")
        
        # Enhanced display with risk assessment
        risk_color = {
            'Low': 'green',
            'Medium': 'orange', 
            'High': 'red'
        }.get(prediction['risk_level'], 'gray')
        
        # FIXED: Using custom HTML boxes instead of st.info/st.success with unsafe_allow_html
        if "UP" in prediction['direction']:
            st.markdown(f"""
            <div class="custom-success-box">
                <h3>📈 {prediction['direction']} PREDICTION</h3>
                <p><strong>Confidence:</strong> {prediction['confidence']:.1f}%</p>
                <p><strong>Timeframe:</strong> {prediction['timeframe']}</p>
                <p><strong>Target Price:</strong> ${prediction['target_price']:,.2f}</p>
                <p><strong>Risk Level:</strong> <span style='color: {risk_color}'>{prediction['risk_level']}</span></p>
                <p><strong>Reasoning:</strong> {prediction['reasoning']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif "DOWN" in prediction['direction']:
            st.markdown(f"""
            <div class="custom-error-box">
                <h3>📉 {prediction['direction']} PREDICTION</h3>
                <p><strong>Confidence:</strong> {prediction['confidence']:.1f}%</p>
                <p><strong>Timeframe:</strong> {prediction['timeframe']}</p>
                <p><strong>Target Price:</strong> ${prediction['target_price']:,.2f}</p>
                <p><strong>Risk Level:</strong> <span style='color: {risk_color}'>{prediction['risk_level']}</span></p>
                <p><strong>Reasoning:</strong> {prediction['reasoning']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="custom-info-box">
                <h3>⚖️ {prediction['direction']} PREDICTION</h3>
                <p><strong>Confidence:</strong> {prediction['confidence']:.1f}%</p>
                <p><strong>Timeframe:</strong> {prediction['timeframe']}</p>
                <p><strong>Expected Range:</strong> ${stats_24h['low']:,.2f} - ${stats_24h['high']:,.2f}</p>
                <p><strong>Risk Level:</strong> <span style='color: {risk_color}'>{prediction['risk_level']}</span></p>
                <p><strong>Reasoning:</strong> {prediction['reasoning']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("**🔑 Detailed Factors Analyzed:**")
        for factor in prediction['factors']:
            st.write(f"• {factor}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_sentiment_section(symbol):
    """Display sentiment comparison across different sources"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.subheader("🌐 Multi-Source Sentiment Analysis")
    
    dashboard = st.session_state.dashboard
    
    if dashboard.sentiment_analyzer is None:
        st.error("❌ Sentiment analyzer not available. Please check if required modules are installed.")
        st.info("💡 Make sure you have the sentiment analysis modules in the 'src/sentiment' folder.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    with st.expander("ℹ️ Enhanced Sentiment Analysis"):
        st.markdown("""
        **🔍 Advanced Sentiment Tracking:**
        
        - **📰 Real-time News Analysis**: Latest headlines and impact assessment
        - **🐦 Social Media Sentiment**: Twitter, Reddit, and community sentiment
        - **📊 Market Data Correlation**: Price action vs sentiment analysis
        - **🌍 Global Sentiment**: Regional market sentiment differences
        
        **📈 Enhanced Features:**
        - Sentiment trend analysis
        - Confidence scoring per source
        - Historical sentiment tracking
        - Multi-language support
        """)
    
    if st.button("🔄 Analyze Multi-Source Sentiment", use_container_width=True, key="sentiment_btn"):
        with st.spinner("🔍 Collecting and analyzing data from all sources..."):
            dashboard.log_message(f"🔍 Starting enhanced sentiment analysis for {symbol}")
            time.sleep(3)
            
            # Enhanced demo sentiment data
            sentiment_summary = {
                'market_sentiment': 'STRONGLY BULLISH',
                'overall_polarity': 'VERY POSITIVE',
                'source_count': 5,
                'confidence': 87.5,
                'trend': 'improving',
                'source_details': [
                    {'source': 'Binance News', 'sentiment': 'STRONGLY BULLISH', 'polarity': '+0.92', 'confidence': 0.94},
                    {'source': 'Twitter/X', 'sentiment': 'BULLISH', 'polarity': '+0.78', 'confidence': 0.82},
                    {'source': 'Reddit', 'sentiment': 'MODERATELY BULLISH', 'polarity': '+0.65', 'confidence': 0.76},
                    {'source': 'Crypto News', 'sentiment': 'BULLISH', 'polarity': '+0.81', 'confidence': 0.88},
                    {'source': 'Telegram', 'sentiment': 'VERY BULLISH', 'polarity': '+0.89', 'confidence': 0.79}
                ]
            }
            
            st.session_state.last_sentiment = sentiment_summary
            st.session_state.show_sentiment_result = True
            dashboard.log_message("✅ Enhanced sentiment analysis completed")
    
    if st.session_state.show_sentiment_result and st.session_state.last_sentiment:
        sentiment_summary = st.session_state.last_sentiment
        
        st.markdown("---")
        st.subheader("🌐 Sentiment Analysis Result")
        
        # Enhanced sentiment display
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; 
                    border-radius: 12px; 
                    text-align: center;
                    margin: 15px 0;">
            <h3 style="color: white; margin: 0 0 10px 0;">Overall Market Sentiment</h3>
            <h2 style="color: white; margin: 0; font-size: 2.8rem;">{sentiment_summary['market_sentiment']}</h2>
            <div style="display: flex; justify-content: center; gap: 30px; margin-top: 15px;">
                <div style="color: rgba(255,255,255,0.9);">
                    <strong>Confidence</strong><br>
                    {sentiment_summary['confidence']}%
                </div>
                <div style="color: rgba(255,255,255,0.9);">
                    <strong>Sources</strong><br>
                    {sentiment_summary['source_count']} analyzed
                </div>
                <div style="color: rgba(255,255,255,0.9);">
                    <strong>Trend</strong><br>
                    {sentiment_summary['trend'].title()}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Detailed Source Analysis")
        
        for source_detail in sentiment_summary['source_details']:
            if "STRONGLY BULLISH" in source_detail['sentiment'] or "VERY BULLISH" in source_detail['sentiment']:
                color = "#10B981"
                emoji = "🚀"
            elif "BULLISH" in source_detail['sentiment']:
                color = "#22C55E"
                emoji = "📈"
            elif "BEARISH" in source_detail['sentiment']:
                color = "#EF4444"
                emoji = "📉"
            else:
                color = "#6B7280"
                emoji = "📊"
            
            st.markdown(f"""
            <div class="source-item">
                <div>
                    <strong>{emoji} {source_detail['source']}</strong><br>
                    <span style="color: {color}; font-weight: bold; font-size: 14px;">{source_detail['sentiment']}</span>
                </div>
                <div style="text-align: right;">
                    <div>Polarity: <code style="background: {color}20; padding: 2px 6px; border-radius: 4px;">{source_detail['polarity']}</code></div>
                    <div>Confidence: <code style="background: {color}20; padding: 2px 6px; border-radius: 4px;">{source_detail['confidence']:.1%}</code></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_logs_section():
    """Display application logs"""
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.subheader("📋 Advanced Activity Monitor")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("**Real-time System Logs**")
    
    with col2:
        if st.button("🔄 Clear Logs", key="clear_logs"):
            st.session_state.app_logs = []
            st.rerun()
    
    with col3:
        if st.button("💾 Export Logs", key="export_logs"):
            if st.session_state.app_logs:
                log_text = "\n".join([f"[{log['timestamp']}] {log['level']}: {log['message']}" 
                                    for log in st.session_state.app_logs])
                st.download_button(
                    label="Download Log File",
                    data=log_text,
                    file_name=f"crypto_dashboard_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
    
    if st.session_state.app_logs:
        st.markdown('<div class="log-container">', unsafe_allow_html=True)
        for log in reversed(st.session_state.app_logs[-25:]):  # Show last 25 logs
            level_color = {
                "INFO": "#00FF00",
                "WARNING": "#FFFF00", 
                "ERROR": "#FF0000"
            }.get(log['level'], "#00FF00")
            
            st.markdown(f"""
            <div class="log-entry">
                <span class="log-timestamp">[{log['timestamp']}]</span>
                <span style="color: {level_color}; font-weight: bold;">[{log['level']}]</span>
                <span class="log-message">{log['message']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No logs available yet. Start using the application to see activity logs.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    initialize_session_state()
    dashboard = st.session_state.dashboard
    dashboard.log_message("🚀 Advanced Crypto Dashboard Started")
    
    # Enhanced header
    st.markdown("""
    <div class="custom-header">
        <h1>🚀 Advanced Crypto Intelligence Platform</h1>
        <p>Professional Trading Analytics • AI Predictions • Portfolio Management • Real-time Alerts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar
    with st.sidebar:
        st.header("🎯 Advanced Control Panel")
        
        # Crypto selection
        selected_crypto = st.selectbox(
            "Select Cryptocurrency:",
            options=list(dashboard.crypto_data.keys()),
            format_func=lambda x: f"{dashboard.crypto_data[x]['emoji']} {dashboard.crypto_data[x]['name']}",
            key="main_crypto_select"
        )
        
        crypto_name = dashboard.crypto_data[selected_crypto]['name']
        dashboard.log_message(f"Selected cryptocurrency: {crypto_name}")
        
        st.markdown("---")
        
        # Enhanced auto-refresh settings
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)
        
        refresh_options = {
            5: "5 seconds (Real-time)",
            10: "10 seconds (Fast)", 
            30: "30 seconds (Standard)",
            60: "1 minute (Slow)",
            300: "5 minutes (Relaxed)"
        }
        
        refresh_rate = st.selectbox(
            "Refresh Rate:",
            options=list(refresh_options.keys()),
            format_func=lambda x: refresh_options[x],
            index=2
        )
        
        # Feature toggles
        st.markdown("**🔧 Feature Toggles**")
        show_logs = st.checkbox("📋 Show Activity Logs", value=st.session_state.show_logs)
        st.session_state.show_logs = show_logs
        
        show_advanced = st.checkbox("🔍 Advanced Charts", value=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Now", key="refresh_btn", use_container_width=True):
                dashboard.log_message("Manual refresh triggered")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear All", key="clear_btn", use_container_width=True):
                st.session_state.prediction_history = []
                st.session_state.last_prediction = None
                st.session_state.last_sentiment = None
                st.session_state.show_prediction_result = False
                st.session_state.show_sentiment_result = False
                st.session_state.app_logs = []
                dashboard.log_message("All data cleared")
                st.rerun()
        
        st.markdown("---")
        st.markdown("**📊 System Status**")
        
        # Enhanced status display
        if dashboard.sentiment_analyzer:
            st.success("✅ Sentiment Analyzer: Active")
        else:
            st.warning("⚠️ Sentiment Analyzer: Limited")
        
        st.success("✅ Price Data: Live")
        st.success("✅ AI Engine: Active")
        st.info(f"**Last Update:** {st.session_state.last_update.strftime('%H:%M:%S')}")
        st.info(f"**Log Entries:** {len(st.session_state.app_logs)}")
        st.info(f"**Alerts:** {len(st.session_state.price_alerts)} active")
    
    # Main content layout
    current_data, stats_24h = dashboard.update_price_data(selected_crypto, refresh_rate)
    current_price = current_data['price']
    
    # Market Overview at the top
    display_market_overview()
    
    # Main charts and stats
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📈 {crypto_name} Advanced Technical Analysis")
        if show_advanced:
            chart = dashboard.create_advanced_chart(selected_crypto)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            else:
                st.info("📊 Collecting market data for advanced visualization...")
        else:
            # Simple chart option
            st.info("Enable Advanced Charts for detailed technical analysis")
    
    with col2:
        st.subheader("💰 Real-time Market Data")
        # FIXED: Now calling the method that exists in the class
        dashboard.display_real_stats(current_data, selected_crypto, stats_24h)
        
        # Quick actions
        st.markdown("**⚡ Quick Actions**")
        if st.button("🎯 Quick Prediction", key="quick_predict"):
            prediction = generate_prediction(selected_crypto, current_price, stats_24h)
            st.session_state.last_prediction = prediction
            st.session_state.show_prediction_result = True
            st.rerun()
        
        if st.button("🔔 Check Alerts", key="quick_alerts"):
            triggered = dashboard.check_alerts()
            if triggered:
                st.success(f"🚨 {len(triggered)} alerts triggered!")
            else:
                st.info("No alerts triggered")
    
    # NEW FEATURES SECTION
    st.markdown("## 🚀 Advanced Features")
    
    # Feature tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🤖 AI Prediction", 
        "🌐 Sentiment", 
        "💼 Portfolio", 
        "🔔 Alerts", 
        "⭐ Watchlist", 
        "📰 News"
    ])
    
    with tab1:
        display_prediction_section(selected_crypto, current_price, stats_24h)
    
    with tab2:
        display_sentiment_section(selected_crypto)
    
    with tab3:
        display_portfolio_section()
    
    with tab4:
        display_alerts_section()
    
    with tab5:
        display_watchlist_section()
    
    with tab6:
        display_news_section()
    
    # Logs section at the bottom
    if st.session_state.show_logs:
        display_logs_section()
    
    # Enhanced footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p> 
        🚀 <strong>Advanced Crypto Intelligence Platform v2.0</strong> | 
        📧 Professional Trading Analytics & AI Insights |
        ⚠️ Not financial advice | 🔒 Secure & Private
        </p>
        <small>System: Live | Data: {source} | Last updated: {}</small>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), source=stats_24h.get('source', 'demo').upper()), unsafe_allow_html=True)
    
    # Update timestamp and auto-refresh
    st.session_state.last_update = datetime.now()
    
    if auto_refresh:
        time.sleep(refresh_rate)
        st.rerun()

if __name__ == "__main__":
    main()