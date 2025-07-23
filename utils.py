"""
Utility functions for SkySentiment Dashboard
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import folium
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

def clean_text(text: str) -> str:
    """
    Clean tweet text by removing mentions, hashtags, URLs, and special characters
    
    Args:
        text (str): Raw tweet text
        
    Returns:
        str: Cleaned text
    """
    if pd.isna(text):
        return ""
    
    # Remove mentions
    text = re.sub(r'@\w+', '', text)
    # Remove hashtags
    text = re.sub(r'#\w+', '', text)
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_hashtags(text: str) -> List[str]:
    """
    Extract hashtags from tweet text
    
    Args:
        text (str): Tweet text
        
    Returns:
        List[str]: List of hashtags
    """
    if pd.isna(text):
        return []
    
    hashtags = re.findall(r'#\w+', text)
    return [tag.lower() for tag in hashtags]

def extract_mentions(text: str) -> List[str]:
    """
    Extract mentions from tweet text
    
    Args:
        text (str): Tweet text
        
    Returns:
        List[str]: List of mentions
    """
    if pd.isna(text):
        return []
    
    mentions = re.findall(r'@\w+', text)
    return [mention.lower() for mention in mentions]

def calculate_engagement_score(row: pd.Series) -> float:
    """
    Calculate engagement score based on retweets and likes
    
    Args:
        row (pd.Series): Tweet row with retweet_count and like_count
        
    Returns:
        float: Engagement score
    """
    retweets = row.get('retweet_count', 0)
    likes = row.get('like_count', 0)
    
    # Weighted score (retweets worth more than likes)
    engagement_score = (retweets * 2) + likes
    return engagement_score

def get_sentiment_color(sentiment: str) -> str:
    """
    Get color for sentiment visualization
    
    Args:
        sentiment (str): Sentiment label
        
    Returns:
        str: Hex color code
    """
    color_map = {
        'Positive': '#2E8B57',
        'Negative': '#DC143C',
        'Neutral': '#4682B4'
    }
    return color_map.get(sentiment, '#666666')

def create_sentiment_pie_chart(data: pd.DataFrame, title: str = "Sentiment Distribution") -> go.Figure:
    """
    Create a pie chart for sentiment distribution
    
    Args:
        data (pd.DataFrame): Data with Predicted_Sentiment column
        title (str): Chart title
        
    Returns:
        go.Figure: Plotly figure object
    """
    sentiment_counts = data['Predicted_Sentiment'].value_counts()
    
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        color=sentiment_counts.index,
        color_discrete_map={
            'Positive': '#2E8B57',
            'Negative': '#DC143C',
            'Neutral': '#4682B4'
        },
        hole=0.4
    )
    
    fig.update_layout(
        title=title,
        showlegend=True,
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

def create_time_series_chart(data: pd.DataFrame, date_column: str = 'date', 
                           value_column: str = 'Predicted_Sentiment') -> go.Figure:
    """
    Create a time series chart for sentiment trends
    
    Args:
        data (pd.DataFrame): Data with date and sentiment columns
        date_column (str): Name of date column
        value_column (str): Name of value column
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Group by date and sentiment
    time_series = data.groupby([data[date_column].dt.date, value_column]).size().unstack(fill_value=0)
    
    fig = px.line(
        time_series,
        title="Sentiment Trends Over Time",
        labels={'value': 'Number of Tweets', 'date': 'Date'}
    )
    
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        xaxis_title="Date",
        yaxis_title="Number of Tweets"
    )
    
    return fig

def create_airline_comparison_chart(data: pd.DataFrame) -> go.Figure:
    """
    Create a comparison chart for airline performance
    
    Args:
        data (pd.DataFrame): Data with Airline and Predicted_Sentiment columns
        
    Returns:
        go.Figure: Plotly figure object
    """
    airline_sentiment = data.groupby(['Airline', 'Predicted_Sentiment']).size().unstack(fill_value=0)
    
    fig = px.bar(
        airline_sentiment,
        title="Airline Sentiment Comparison",
        barmode='group',
        color_discrete_map={
            'Positive': '#2E8B57',
            'Negative': '#DC143C',
            'Neutral': '#4682B4'
        }
    )
    
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        xaxis_title="Airline",
        yaxis_title="Number of Tweets"
    )
    
    return fig

def create_wordcloud(text_data: pd.Series, max_words: int = 100) -> WordCloud:
    """
    Create a word cloud from text data
    
    Args:
        text_data (pd.Series): Series of text data
        max_words (int): Maximum number of words to include
        
    Returns:
        WordCloud: WordCloud object
    """
    # Combine all text
    text = ' '.join(text_data.astype(str))
    
    # Clean text
    text = clean_text(text)
    
    # Create wordcloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=max_words,
        colormap='viridis',
        stopwords=set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    ).generate(text)
    
    return wordcloud

def create_interactive_map(data: pd.DataFrame, max_points: int = 100) -> folium.Map:
    """
    Create an interactive map with tweet locations
    
    Args:
        data (pd.DataFrame): Data with latitude, longitude, and sentiment columns
        max_points (int): Maximum number of points to show
        
    Returns:
        folium.Map: Folium map object
    """
    # Filter data with valid coordinates
    geo_data = data.dropna(subset=['latitude', 'longitude'])
    
    if len(geo_data) == 0:
        return None
    
    # Limit points for performance
    if len(geo_data) > max_points:
        geo_data = geo_data.sample(n=max_points, random_state=42)
    
    # Create map
    m = folium.Map(
        location=[geo_data['latitude'].mean(), geo_data['longitude'].mean()],
        zoom_start=5,
        tiles='OpenStreetMap'
    )
    
    # Add markers
    for idx, row in geo_data.iterrows():
        color = get_sentiment_color(row['Predicted_Sentiment'])
        
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color=color,
            fill=True,
            popup=f"""
            <b>Airline:</b> {row['Airline']}<br>
            <b>Sentiment:</b> {row['Predicted_Sentiment']}<br>
            <b>Location:</b> {row.get('tweet_location', 'Unknown')}<br>
            <b>Confidence:</b> {row.get('Sentiment_Confidence', 0):.3f}
            """
        ).add_to(m)
    
    return m

def calculate_airline_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate comprehensive metrics for each airline
    
    Args:
        data (pd.DataFrame): Data with airline and sentiment information
        
    Returns:
        pd.DataFrame: DataFrame with airline metrics
    """
    metrics = data.groupby('Airline').agg({
        'Predicted_Sentiment': lambda x: (x == 'Positive').mean() * 100,
        'Sentiment_Confidence': 'mean',
        'retweet_count': ['mean', 'sum'],
        'like_count': ['mean', 'sum'],
        'tweet_content': 'count'
    }).round(2)
    
    # Flatten column names
    metrics.columns = [
        'Positive_Sentiment_%', 'Avg_Confidence', 
        'Avg_Retweets', 'Total_Retweets',
        'Avg_Likes', 'Total_Likes', 'Total_Tweets'
    ]
    
    # Calculate additional metrics
    metrics['Engagement_Rate'] = ((metrics['Total_Retweets'] + metrics['Total_Likes']) / metrics['Total_Tweets']).round(2)
    metrics['Negative_Sentiment_%'] = (data.groupby('Airline')['Predicted_Sentiment'].apply(lambda x: (x == 'Negative').mean() * 100)).round(2)
    
    return metrics

def get_trend_analysis(data: pd.DataFrame, days: int = 7) -> Dict:
    """
    Perform trend analysis on sentiment data
    
    Args:
        data (pd.DataFrame): Data with date and sentiment columns
        days (int): Number of days to analyze
        
    Returns:
        Dict: Dictionary with trend analysis results
    """
    # Get recent data
    recent_date = data['date'].max()
    start_date = recent_date - timedelta(days=days)
    recent_data = data[data['date'] >= start_date]
    
    # Calculate daily trends
    daily_sentiment = recent_data.groupby([recent_data['date'].dt.date, 'Predicted_Sentiment']).size().unstack(fill_value=0)
    
    # Calculate trends
    trends = {}
    for sentiment in ['Positive', 'Negative', 'Neutral']:
        if sentiment in daily_sentiment.columns:
            values = daily_sentiment[sentiment].values
            if len(values) > 1:
                trend = (values[-1] - values[0]) / len(values)
                trends[sentiment] = {
                    'trend': trend,
                    'direction': 'increasing' if trend > 0 else 'decreasing' if trend < 0 else 'stable',
                    'change_pct': ((values[-1] - values[0]) / max(values[0], 1)) * 100
                }
    
    return trends

def format_number(num: float) -> str:
    """
    Format number for display
    
    Args:
        num (float): Number to format
        
    Returns:
        str: Formatted number string
    """
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:.0f}"

def validate_data(data: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate data for required columns and data types
    
    Args:
        data (pd.DataFrame): Data to validate
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, error_messages)
    """
    required_columns = [
        'date', 'user', 'tweet_content', 'Airline', 
        'Predicted_Sentiment', 'Sentiment_Confidence'
    ]
    
    errors = []
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")
    
    # Check data types
    if 'date' in data.columns:
        try:
            pd.to_datetime(data['date'])
        except:
            errors.append("Date column contains invalid dates")
    
    if 'Sentiment_Confidence' in data.columns:
        if not pd.api.types.is_numeric_dtype(data['Sentiment_Confidence']):
            errors.append("Sentiment_Confidence must be numeric")
    
    # Check sentiment values
    if 'Predicted_Sentiment' in data.columns:
        valid_sentiments = ['Positive', 'Negative', 'Neutral']
        invalid_sentiments = data['Predicted_Sentiment'].unique()
        invalid_sentiments = [s for s in invalid_sentiments if s not in valid_sentiments]
        if invalid_sentiments:
            errors.append(f"Invalid sentiment values: {invalid_sentiments}")
    
    return len(errors) == 0, errors

def get_data_summary(data: pd.DataFrame) -> Dict:
    """
    Get comprehensive data summary
    
    Args:
        data (pd.DataFrame): Data to summarize
        
    Returns:
        Dict: Summary statistics
    """
    summary = {
        'total_tweets': len(data),
        'date_range': {
            'start': data['date'].min().strftime('%Y-%m-%d'),
            'end': data['date'].max().strftime('%Y-%m-%d')
        },
        'airlines': data['Airline'].nunique(),
        'users': data['user'].nunique(),
        'sentiment_distribution': data['Predicted_Sentiment'].value_counts().to_dict(),
        'avg_confidence': data['Sentiment_Confidence'].mean(),
        'total_engagement': {
            'retweets': data['retweet_count'].sum(),
            'likes': data['like_count'].sum()
        },
        'geographic_coverage': {
            'locations': data['tweet_location'].nunique(),
            'valid_coordinates': data.dropna(subset=['latitude', 'longitude']).shape[0]
        }
    }
    
    return summary 