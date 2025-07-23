import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
from collections import Counter
import random
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="SkySentiment - Indian Airline Tweet Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with animations
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0e1117 0%, #1a1a2e 50%, #16213e 100%);
        color: #fafafa;
        animation: gradientShift 10s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1a2e 50%, #16213e 100%);
        background-size: 400% 400%;
        animation: gradientShift 10s ease-in-out infinite;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #00d4ff, #ff6b35, #ffd700, #00d4ff);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientFlow 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
    }
    
    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #b0b0b0;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #00d4ff;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.3);
        border-left: 4px solid #ffd700;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(45deg, #00d4ff, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .metric-label {
        color: #b0b0b0;
        font-size: 0.9rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        animation: slideInLeft 0.8s ease-out;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .airline-card {
        background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin: 0.5rem 0;
        border: 1px solid #333;
    }
    
    .airline-card h4 {
        color: #00d4ff;
        margin-bottom: 0.5rem;
    }
    
    .airline-card p {
        color: #b0b0b0;
        margin: 0.25rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        border-radius: 12px;
        padding: 6px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: linear-gradient(135deg, #2a2a2a, #3a3a3a);
        border-radius: 8px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #b0b0b0;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #3a3a3a, #4a4a4a);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        left: 100%;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff, #ff6b35);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
        animation: tabGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes tabGlow {
        from { box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4); }
        to { box-shadow: 0 4px 20px rgba(0, 212, 255, 0.6); }
    }
    
    .section-header {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #00d4ff;
    }
    
    .sidebar-header {
        color: #00d4ff;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .filter-label {
        color: #b0b0b0;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #0099cc);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0099cc, #006699);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 212, 255, 0.3);
    }
    
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem;
        border-top: 1px solid #333;
        margin-top: 2rem;
    }
    
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; }
        .metric-card { padding: 1rem; }
        .metric-value { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# Utility functions
def load_data():
    """Load and preprocess data with caching"""
    try:
data = pd.read_csv('sentiment_analyzed_data.csv', encoding='latin-1')
        data['date'] = pd.to_datetime(data['date'])
        data['Date'] = data['date']
        data['tweet_location'] = data['tweet_location'].fillna('Unknown')
        data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
        data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')
        data['hour'] = data['date'].dt.hour
        data['day_of_week'] = data['date'].dt.day_name()
        data['month'] = data['date'].dt.month
        data['year'] = data['date'].dt.year
        data['Airline'] = data['Airline'].str.title()
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def extract_hashtags(text):
    """Extract hashtags from text"""
    if pd.isna(text):
        return []
    hashtags = re.findall(r'#\w+', str(text))
    return [tag.lower() for tag in hashtags]

def create_chart_config():
    """Create consistent chart configuration"""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': dict(color='#fafafa'),
        'xaxis': dict(gridcolor='#333'),
        'yaxis': dict(gridcolor='#333')
    }

# Load data
@st.cache_data
def cached_load_data():
    return load_data()

data = cached_load_data()

if data is None:
    st.error("Failed to load data. Please check if 'sentiment_analyzed_data.csv' exists.")
    st.stop()

# Main header
st.markdown('<h1 class="main-header">✈️ SkySentiment Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🚀 Comprehensive Indian Airline Tweet Sentiment Analysis Platform 🚀</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<h3 class="sidebar-header">🎛️ Dashboard Controls</h3>', unsafe_allow_html=True)
st.sidebar.markdown("---")

# Filters
st.sidebar.markdown('<p class="filter-label">📅 Date Range</p>', unsafe_allow_html=True)
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(data['date'].min().date(), data['date'].max().date()),
    min_value=data['date'].min().date(),
    max_value=data['date'].max().date(),
    label_visibility="collapsed"
)

st.sidebar.markdown('<p class="filter-label">🛫 Airlines</p>', unsafe_allow_html=True)
all_airlines = ['All'] + sorted(data['Airline'].unique().tolist())
selected_airlines = st.sidebar.multiselect(
    "Select Airlines",
    options=all_airlines,
    default=['All'],
    label_visibility="collapsed"
)

st.sidebar.markdown('<p class="filter-label">😊 Sentiment</p>', unsafe_allow_html=True)
sentiment_options = ['All', 'Positive', 'Negative', 'Neutral']
selected_sentiments = st.sidebar.multiselect(
    "Select Sentiments",
    options=sentiment_options,
    default=['All'],
    label_visibility="collapsed"
)

# Apply filters
filtered_data = data.copy()

if len(date_range) == 2:
    filtered_data = filtered_data[
        (filtered_data['date'].dt.date >= date_range[0]) &
        (filtered_data['date'].dt.date <= date_range[1])
    ]

if 'All' not in selected_airlines:
    filtered_data = filtered_data[filtered_data['Airline'].isin(selected_airlines)]

if 'All' not in selected_sentiments:
    filtered_data = filtered_data[filtered_data['Predicted_Sentiment'].isin(selected_sentiments)]

# Main content with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "📈 Trends & Analytics", 
    "🏢 Airline Comparison", 
    "📝 Content Analysis", 
    "🔍 Deep Dive"
])

# Tab 1: Overview
with tab1:
    st.markdown('<h2 class="section-header">📊 Executive Summary</h2>', unsafe_allow_html=True)
    
    # Fun interactive element
    if st.button("🎲 Click for a Random Insight!", key="random_insight"):
        insights = [
            "🌟 Did you know? Most tweets are posted during business hours!",
            "🎯 Pro tip: Use the date filter to see how sentiment changes over time!",
            "🚀 Fun fact: This dashboard processes data in real-time!",
            "💡 Insight: Geographic analysis reveals regional sentiment patterns!",
            "🎨 Cool feature: Try hovering over the metric cards for cool effects!",
            "🔍 Pro tip: Use the deep dive tab to explore individual tweets!",
            "📈 Insight: Engagement metrics show which content resonates most!",
            "🎪 Fun fact: The word clouds reveal trending topics automatically!"
        ]
        st.balloons()
        st.success(f"🎉 {random.choice(insights)}")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_tweets = len(filtered_data)
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{total_tweets:,}</p>
            <p class="metric-label">Total Tweets</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        positive_pct = (filtered_data['Predicted_Sentiment'] == 'Positive').mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{positive_pct:.1f}%</p>
            <p class="metric-label">Positive Sentiment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        negative_pct = (filtered_data['Predicted_Sentiment'] == 'Negative').mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{negative_pct:.1f}%</p>
            <p class="metric-label">Negative Sentiment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_confidence = filtered_data['Sentiment_Confidence'].mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{avg_confidence:.1f}%</p>
            <p class="metric-label">Avg Confidence</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sentiment distribution
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h3 class="section-header">Sentiment Distribution</h3>', unsafe_allow_html=True)
        sentiment_counts = filtered_data['Predicted_Sentiment'].value_counts()
        
        fig = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            color_discrete_map={
                'Positive': '#00d4ff',
                'Negative': '#ff6b35',
                'Neutral': '#6c757d'
            },
            hole=0.4
        )
        fig.update_layout(
            title="",
            showlegend=True,
            height=400,
            **create_chart_config()
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="section-header">Sentiment Breakdown</h3>', unsafe_allow_html=True)
        for sentiment, count in sentiment_counts.items():
            percentage = (count / total_tweets) * 100
            color = {
                'Positive': '#00d4ff',
                'Negative': '#ff6b35',
                'Neutral': '#6c757d'
            }.get(sentiment, '#666')
            
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {color}; margin: 0;">{sentiment}</h4>
                <p style="font-size: 1.5rem; font-weight: bold; margin: 0; color: #fafafa;">{count:,}</p>
                <p style="color: #b0b0b0; margin: 0;">{percentage:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Airline performance overview
    st.markdown('<h3 class="section-header">Airline Performance Overview</h3>', unsafe_allow_html=True)
    
    airline_sentiment = filtered_data.groupby(['Airline', 'Predicted_Sentiment']).size().unstack(fill_value=0)
    airline_sentiment['Total'] = airline_sentiment.sum(axis=1)
    airline_sentiment['Positive_Pct'] = (airline_sentiment['Positive'] / airline_sentiment['Total']) * 100
    airline_sentiment['Negative_Pct'] = (airline_sentiment['Negative'] / airline_sentiment['Total']) * 100
    
    fig = px.bar(
        airline_sentiment,
        x=airline_sentiment.index,
        y=['Positive_Pct', 'Negative_Pct'],
        title="",
        barmode='group',
        color_discrete_map={
            'Positive_Pct': '#00d4ff',
            'Negative_Pct': '#ff6b35'
        }
    )
    fig.update_layout(
        xaxis_title="Airline",
        yaxis_title="Percentage (%)",
        height=400,
        **create_chart_config()
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights Section
    st.markdown('<h3 class="section-header">💡 Key Insights</h3>', unsafe_allow_html=True)
    
    # Calculate insights
    total_tweets = len(filtered_data)
    positive_tweets = len(filtered_data[filtered_data['Predicted_Sentiment'] == 'Positive'])
    negative_tweets = len(filtered_data[filtered_data['Predicted_Sentiment'] == 'Negative'])
    neutral_tweets = len(filtered_data[filtered_data['Predicted_Sentiment'] == 'Neutral'])
    
    # Find top airline by positive sentiment
    airline_positive = filtered_data[filtered_data['Predicted_Sentiment'] == 'Positive']['Airline'].value_counts()
    top_positive_airline = airline_positive.index[0] if len(airline_positive) > 0 else "N/A"
    
    # Find most active hour
    peak_hour = filtered_data['hour'].value_counts().index[0] if len(filtered_data) > 0 else "N/A"
    
    # Find average tweet length
    avg_tweet_length = filtered_data['tweet_content'].str.len().mean()
    
    # Find average confidence
    avg_confidence = filtered_data['Sentiment_Confidence'].mean() * 100
    
    # Create insights cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #00d4ff; margin: 0;">📊 Overall Sentiment</h4>
            <p style="color: #fafafa; margin: 0.5rem 0;">Positive: {positive_tweets:,} tweets ({positive_tweets/total_tweets*100:.1f}%)</p>
            <p style="color: #fafafa; margin: 0.5rem 0;">Negative: {negative_tweets:,} tweets ({negative_tweets/total_tweets*100:.1f}%)</p>
            <p style="color: #fafafa; margin: 0.5rem 0;">Neutral: {neutral_tweets:,} tweets ({neutral_tweets/total_tweets*100:.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #ff6b35; margin: 0;">🏆 Top Performer</h4>
            <p style="color: #fafafa; margin: 0.5rem 0;">Most Positive: <strong>{top_positive_airline}</strong></p>
            <p style="color: #b0b0b0; margin: 0.5rem 0;">Leading with highest positive sentiment ratio</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #ffd700; margin: 0;">⏰ Activity Patterns</h4>
            <p style="color: #fafafa; margin: 0.5rem 0;">Peak Hour: <strong>{peak_hour}:00</strong></p>
            <p style="color: #fafafa; margin: 0.5rem 0;">Avg Tweet Length: <strong>{avg_tweet_length:.0f} characters</strong></p>
            <p style="color: #fafafa; margin: 0.5rem 0;">Confidence: <strong>{avg_confidence:.1f}%</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #6c757d; margin: 0;">📈 Data Quality</h4>
            <p style="color: #fafafa; margin: 0.5rem 0;">Total Tweets: <strong>{total_tweets:,}</strong></p>
            <p style="color: #fafafa; margin: 0.5rem 0;">Airlines Covered: <strong>{len(filtered_data['Airline'].unique())}</strong></p>
            <p style="color: #b0b0b0; margin: 0.5rem 0;">Real-time sentiment analysis</p>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Trends & Analytics
with tab2:
    st.markdown('<h2 class="section-header">📈 Temporal Trends & Analytics</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-header">Sentiment Trends Over Time</h3>', unsafe_allow_html=True)
        
        daily_sentiment = filtered_data.groupby([filtered_data['date'].dt.date, 'Predicted_Sentiment']).size().unstack(fill_value=0)
        
        fig = px.line(
            daily_sentiment,
            title="",
            labels={'value': 'Number of Tweets', 'date': 'Date'},
            color_discrete_map={
                'Positive': '#00d4ff',
                'Negative': '#ff6b35',
                'Neutral': '#6c757d'
            }
        )
        fig.update_layout(height=400, **create_chart_config())
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="section-header">Hourly Activity Pattern</h3>', unsafe_allow_html=True)
        
        hourly_activity = filtered_data['hour'].value_counts().sort_index()
        
        fig = px.bar(
            x=hourly_activity.index,
            y=hourly_activity.values,
            title="",
            labels={'x': 'Hour', 'y': 'Number of Tweets'},
            color_discrete_sequence=['#00d4ff']
        )
        fig.update_layout(height=400, **create_chart_config())
        st.plotly_chart(fig, use_container_width=True)
    
    # Weekly patterns
    st.markdown('<h3 class="section-header">Weekly Activity Patterns</h3>', unsafe_allow_html=True)
    
    weekly_sentiment = filtered_data.groupby(['day_of_week', 'Predicted_Sentiment']).size().unstack(fill_value=0)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_sentiment = weekly_sentiment.reindex(day_order)
    
    fig = px.bar(
        weekly_sentiment,
        title="",
        barmode='group',
        color_discrete_map={
            'Positive': '#00d4ff',
            'Negative': '#ff6b35',
            'Neutral': '#6c757d'
        }
    )
    fig.update_layout(height=400, **create_chart_config())
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Airline Comparison
with tab3:
    st.markdown('<h2 class="section-header">🏢 Airline Performance Comparison</h2>', unsafe_allow_html=True)
    
    # Airline metrics
    airline_metrics = filtered_data.groupby('Airline').agg({
        'Predicted_Sentiment': lambda x: (x == 'Positive').mean() * 100,
        'Sentiment_Confidence': 'mean',
        'retweet_count': 'mean',
        'like_count': 'mean'
    }).round(2)
    
    airline_metrics.columns = ['Positive_Sentiment_%', 'Avg_Confidence', 'Avg_Retweets', 'Avg_Likes']
    airline_metrics['Total_Tweets'] = filtered_data['Airline'].value_counts()
    
    st.markdown('<h3 class="section-header">Airline Performance Metrics</h3>', unsafe_allow_html=True)
    st.dataframe(airline_metrics, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-header">Sentiment Distribution by Airline</h3>', unsafe_allow_html=True)
        
        airline_sentiment_pivot = filtered_data.groupby(['Airline', 'Predicted_Sentiment']).size().unstack(fill_value=0)
        
        fig = px.bar(
            airline_sentiment_pivot,
            title="",
            barmode='group',
            color_discrete_map={
                'Positive': '#00d4ff',
                'Negative': '#ff6b35',
                'Neutral': '#6c757d'
            }
        )
        fig.update_layout(height=400, **create_chart_config())
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="section-header">Positive Sentiment Percentage</h3>', unsafe_allow_html=True)
        
        positive_pct = airline_metrics['Positive_Sentiment_%'].sort_values(ascending=True)
        
        fig = px.bar(
            x=positive_pct.values,
            y=positive_pct.index,
            orientation='h',
            title="",
            labels={'x': 'Positive Sentiment (%)', 'y': 'Airline'},
            color_discrete_sequence=['#00d4ff']
        )
        fig.update_layout(height=400, **create_chart_config())
        st.plotly_chart(fig, use_container_width=True)

# Tab 4: Content Analysis
with tab4:
    st.markdown('<h2 class="section-header">📝 Content Analysis</h2>', unsafe_allow_html=True)
    
    # Hashtag analysis
    st.markdown('<h3 class="section-header">Hashtag Analysis</h3>', unsafe_allow_html=True)
    
    all_hashtags = []
    for text in filtered_data['tweet_content']:
        all_hashtags.extend(extract_hashtags(text))
    
    if all_hashtags:
        hashtag_counts = Counter(all_hashtags)
        top_hashtags = dict(hashtag_counts.most_common(15))
        
        fig = px.bar(
            x=list(top_hashtags.values()),
            y=list(top_hashtags.keys()),
            orientation='h',
            title="",
            labels={'x': 'Count', 'y': 'Hashtag'},
            color_discrete_sequence=['#00d4ff']
        )
        fig.update_layout(height=400, **create_chart_config())
        st.plotly_chart(fig, use_container_width=True)
else:
        st.info("No hashtags found in the selected data.")
    
    # Tweet length analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-header">Tweet Length Distribution</h3>', unsafe_allow_html=True)
        
        tweet_lengths = filtered_data['tweet_content'].str.len()
        
        fig = px.histogram(
            x=tweet_lengths,
            title="",
            labels={'x': 'Tweet Length (characters)'},
            color_discrete_sequence=['#00d4ff']
        )
        fig.update_layout(height=400, **create_chart_config())
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="section-header">Average Tweet Length by Sentiment</h3>', unsafe_allow_html=True)
        
        avg_length_by_sentiment = filtered_data.groupby('Predicted_Sentiment')['tweet_content'].apply(lambda x: x.str.len().mean())
        
        fig = px.bar(
            x=avg_length_by_sentiment.index,
            y=avg_length_by_sentiment.values,
            title="",
            labels={'x': 'Sentiment', 'y': 'Average Length (characters)'},
            color_discrete_sequence=['#00d4ff']
        )
        fig.update_layout(height=400, **create_chart_config())
        st.plotly_chart(fig, use_container_width=True)

# Tab 5: Deep Dive
with tab5:
    st.markdown('<h2 class="section-header">🔍 Deep Dive Analysis</h2>', unsafe_allow_html=True)
    
    # Sample tweets display
    st.markdown('<h3 class="section-header">Sample Tweets by Sentiment</h3>', unsafe_allow_html=True)
    
    sentiment_choice = st.selectbox("Select Sentiment to View Sample Tweets:", ['Positive', 'Negative', 'Neutral'])
    
    sample_tweets = filtered_data[filtered_data['Predicted_Sentiment'] == sentiment_choice][['tweet_content', 'Airline', 'date', 'Sentiment_Confidence']].head(10)
    
    for idx, tweet in sample_tweets.iterrows():
        confidence_color = '#00d4ff' if tweet['Sentiment_Confidence'] > 0.7 else '#ff6b35' if tweet['Sentiment_Confidence'] > 0.5 else '#6c757d'
        
        st.markdown(f"""
        <div class="airline-card">
            <h4 style="color: #00d4ff;">{tweet['Airline']}</h4>
            <p style="color: #b0b0b0;"><strong>Date:</strong> {tweet['date'].strftime('%Y-%m-%d %H:%M')}</p>
            <p style="color: #b0b0b0;"><strong>Confidence:</strong> <span style="color: {confidence_color};">{tweet['Sentiment_Confidence']:.3f}</span></p>
            <p style="color: #fafafa;"><strong>Tweet:</strong> {tweet['tweet_content'][:200]}{'...' if len(tweet['tweet_content']) > 200 else ''}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Advanced filtering
    st.markdown('<h3 class="section-header">Advanced Data Explorer</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_confidence = st.slider("Minimum Confidence Score", 0.0, 1.0, 0.0, 0.1)
        min_retweets = st.slider("Minimum Retweets", 0, 100, 0)
    
    with col2:
        min_likes = st.slider("Minimum Likes", 0, 100, 0)
        show_raw_data = st.checkbox("Show Raw Data")
    
    # Apply advanced filters
    advanced_filtered = filtered_data[
        (filtered_data['Sentiment_Confidence'] >= min_confidence) &
        (filtered_data['retweet_count'] >= min_retweets) &
        (filtered_data['like_count'] >= min_likes)
    ]
    
    st.markdown(f'<p style="color: #b0b0b0;"><strong>Filtered Results:</strong> {len(advanced_filtered)} tweets</p>', unsafe_allow_html=True)
    
    if show_raw_data and len(advanced_filtered) > 0:
        st.dataframe(advanced_filtered[['date', 'user', 'tweet_content', 'Airline', 'Predicted_Sentiment', 'Sentiment_Confidence', 'retweet_count', 'like_count']], use_container_width=True)
    
    # Export functionality
    st.markdown('<h3 class="section-header">Export Data</h3>', unsafe_allow_html=True)
    
    if st.button("Export Filtered Data to CSV"):
        csv = advanced_filtered.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"airline_sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>✈️ SkySentiment Dashboard | Indian Airline Tweet Sentiment Analysis</p>
    <p>🚀 Built with Streamlit | Data updated in real-time | Made with ❤️ and ☕</p>
    <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">
        🎉 Thanks for exploring! This is the optimized version with minimal dependencies! 🎯
    </p>
</div>
""", unsafe_allow_html=True)

# Easter egg
if st.button("🥚 Easter Egg", key="easter_egg"):
    st.balloons()
    st.success("🎉 You found the secret! This optimized dashboard is powered by lightweight magic! ✨") 