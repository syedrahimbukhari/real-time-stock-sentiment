import streamlit as st
from datetime import datetime
import time

class DashboardHelpers:
    @staticmethod
    def setup_custom_css():
        """Setup custom CSS for better styling"""
        st.markdown("""
        <style>
        /* Main background */
        .main {
            background-color: #0E1117;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #262730;
        }
        
        /* Metric cards styling */
        .stMetric {
            background-color: #1E1E1E;
            border-radius: 10px;
            padding: 10px;
        }
        
        /* Success, Error, Info boxes */
        .stSuccess {
            background-color: #1E3A1E;
            border-left: 5px solid #28A745;
        }
        
        .stError {
            background-color: #3A1E1E;
            border-left: 5px solid #DC3545;
        }
        
        .stInfo {
            background-color: #1E2E3A;
            border-left: 5px solid #17A2B8;
        }
        
        /* Custom header */
        .custom-header {
            background: linear-gradient(90deg, #FF4B4B, #FF8C42);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            font-size: 2.5rem;
        }
        
        /* Loading animation */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_metric_card(label, value, delta=None, delta_color="normal"):
        """Create a styled metric card"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.metric(
                label=label,
                value=value,
                delta=delta,
                delta_color=delta_color
            )
    
    @staticmethod
    def display_loading_animation(message="Loading..."):
        """Display a loading animation"""
        with st.spinner(f"🔄 {message}"):
            time.sleep(0.5)
    
    @staticmethod
    def create_section_header(title, emoji):
        """Create a styled section header"""
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #1E3A8A, #3B82F6); 
                    padding: 15px; 
                    border-radius: 10px; 
                    margin: 10px 0;">
            <h3 style="color: white; margin: 0; display: flex; align-items: center;">
                <span style="font-size: 1.5em; margin-right: 10px;">{emoji}</span>
                {title}
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def format_timestamp(timestamp):
        """Format timestamp for display"""
        if isinstance(timestamp, str):
            return timestamp
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_color_for_sentiment(sentiment):
        """Get color based on sentiment"""
        colors = {
            "Positive": "#28A745",  # Green
            "Negative": "#DC3545",  # Red
            "Neutral": "#6C757D"    # Gray
        }
        return colors.get(sentiment, "#6C757D")
    
    @staticmethod
    def get_emoji_for_sentiment(sentiment):
        """Get emoji based on sentiment"""
        emojis = {
            "Positive": "😊",
            "Negative": "😠", 
            "Neutral": "😐"
        }
        return emojis.get(sentiment, "😐")

# Test function
def test_helpers():
    """Test dashboard helpers"""
    print("🧪 Testing Dashboard Helpers...")
    
    helpers = DashboardHelpers()
    
    # Test color mapping
    print(f"✅ Positive color: {helpers.get_color_for_sentiment('Positive')}")
    print(f"✅ Negative color: {helpers.get_color_for_sentiment('Negative')}")
    print(f"✅ Neutral color: {helpers.get_color_for_sentiment('Neutral')}")
    
    # Test emoji mapping
    print(f"✅ Positive emoji: {helpers.get_emoji_for_sentiment('Positive')}")
    print(f"✅ Negative emoji: {helpers.get_emoji_for_sentiment('Negative')}")
    print(f"✅ Neutral emoji: {helpers.get_emoji_for_sentiment('Neutral')}")
    
    print("✅ Helpers test completed successfully")

if __name__ == "__main__":
    test_helpers()