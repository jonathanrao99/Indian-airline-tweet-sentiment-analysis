"""
Test script for SkySentiment Dashboard
"""

import pandas as pd
import sys
import os
from datetime import datetime

def test_data_loading():
    """Test if data can be loaded correctly"""
    print("Testing data loading...")
    
    try:
        # Check if data file exists
        if not os.path.exists('sentiment_analyzed_data.csv'):
            print("❌ Error: sentiment_analyzed_data.csv not found")
            return False
        
        # Load data
        data = pd.read_csv('sentiment_analyzed_data.csv', encoding='latin-1')
        print(f"✅ Data loaded successfully: {len(data)} rows, {len(data.columns)} columns")
        
        # Check required columns
        required_columns = [
            'date', 'user', 'tweet_content', 'Airline', 
            'Predicted_Sentiment', 'Sentiment_Confidence'
        ]
        
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            return False
        
        print("✅ All required columns present")
        
        # Check data types
        try:
            data['date'] = pd.to_datetime(data['date'])
            print("✅ Date column converted successfully")
        except Exception as e:
            print(f"❌ Error converting date column: {e}")
            return False
        
        # Check sentiment values
        valid_sentiments = ['Positive', 'Negative', 'Neutral']
        actual_sentiments = data['Predicted_Sentiment'].unique()
        invalid_sentiments = [s for s in actual_sentiments if s not in valid_sentiments]
        
        if invalid_sentiments:
            print(f"⚠️  Warning: Invalid sentiment values found: {invalid_sentiments}")
        else:
            print("✅ All sentiment values are valid")
        
        # Check confidence scores
        if 'Sentiment_Confidence' in data.columns:
            confidence_range = (data['Sentiment_Confidence'].min(), data['Sentiment_Confidence'].max())
            print(f"✅ Confidence scores range: {confidence_range}")
        
        # Check airlines
        airlines = data['Airline'].unique()
        print(f"✅ Airlines found: {list(airlines)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    print("\nTesting dependencies...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 
        'matplotlib', 'seaborn', 'wordcloud', 'folium'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {missing_packages}")
        print("Install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available")
    return True

def test_data_quality():
    """Test data quality metrics"""
    print("\nTesting data quality...")
    
    try:
        data = pd.read_csv('sentiment_analyzed_data.csv', encoding='latin-1')
        
        # Check for missing values
        missing_data = data.isnull().sum()
        total_missing = missing_data.sum()
        
        if total_missing > 0:
            print(f"⚠️  Missing values found: {total_missing}")
            print("Missing values per column:")
            for col, missing in missing_data[missing_data > 0].items():
                print(f"  {col}: {missing}")
        else:
            print("✅ No missing values found")
        
        # Check data distribution
        print(f"\nData distribution:")
        print(f"  Total tweets: {len(data)}")
        print(f"  Date range: {data['date'].min()} to {data['date'].max()}")
        print(f"  Airlines: {data['Airline'].nunique()}")
        print(f"  Users: {data['user'].nunique()}")
        
        # Sentiment distribution
        sentiment_dist = data['Predicted_Sentiment'].value_counts()
        print(f"\nSentiment distribution:")
        for sentiment, count in sentiment_dist.items():
            percentage = (count / len(data)) * 100
            print(f"  {sentiment}: {count} ({percentage:.1f}%)")
        
        # Geographic data
        if 'latitude' in data.columns and 'longitude' in data.columns:
            geo_data = data.dropna(subset=['latitude', 'longitude'])
            print(f"\nGeographic data:")
            print(f"  Tweets with coordinates: {len(geo_data)} ({len(geo_data)/len(data)*100:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in data quality test: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SkySentiment Dashboard - Test Suite")
    print("=" * 50)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    # Test data loading
    data_ok = test_data_loading()
    
    # Test data quality
    quality_ok = test_data_quality()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"  Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print(f"  Data Loading: {'✅ PASS' if data_ok else '❌ FAIL'}")
    print(f"  Data Quality: {'✅ PASS' if quality_ok else '❌ FAIL'}")
    
    if deps_ok and data_ok and quality_ok:
        print("\n🎉 All tests passed! The dashboard should work correctly.")
        print("\nTo run the dashboard:")
        print("  streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before running the dashboard.")
        sys.exit(1)

if __name__ == "__main__":
    main() 