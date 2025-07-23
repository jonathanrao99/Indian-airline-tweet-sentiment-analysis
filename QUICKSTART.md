# 🚀 Quick Start Guide - SkySentiment Dashboard

Get your Indian Airline Tweet Sentiment Analysis dashboard up and running in minutes!

## ⚡ Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Setup
```bash
python test_app.py
```

### 3. Launch Dashboard
```bash
streamlit run app.py
```

### 4. Open Browser
Navigate to: `http://localhost:8501`

## 📋 Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- **sentiment_analyzed_data.csv** file in the project directory

## 🔧 Troubleshooting

### Common Issues

**❌ "Module not found" errors**
```bash
pip install -r requirements.txt
```

**❌ "Data file not found"**
- Ensure `sentiment_analyzed_data.csv` is in the same directory as `app.py`
- Check file permissions

**❌ "Port already in use"**
```bash
streamlit run app.py --server.port 8502
```

**❌ "Memory issues with large datasets"**
- Reduce data size or increase system memory
- Use data sampling in the app

## 🎯 First Steps

1. **Explore Overview Tab** - Get familiar with key metrics
2. **Try Filters** - Use sidebar to filter by date, airline, or sentiment
3. **View Trends** - Check the Trends & Analytics tab
4. **Explore Geography** - See tweet locations on the map
5. **Compare Airlines** - Use the Airline Comparison tab

## 📊 Key Features to Try

### 📈 Real-time Analytics
- Filter by date range to see trends
- Compare different airlines
- Analyze sentiment patterns

### 🗺️ Geographic Analysis
- View tweet locations on interactive map
- Identify regional sentiment patterns
- Explore location-based insights

### 📝 Content Analysis
- Generate word clouds for different sentiments
- Analyze hashtag usage
- Explore tweet content patterns

### 🔍 Deep Dive
- View sample tweets by sentiment
- Export filtered data
- Advanced filtering options

## 🎨 Customization

### Modify Colors
Edit `config.py` to change the color scheme:
```python
VIZ_CONFIG = {
    'color_scheme': {
        'positive': '#2E8B57',
        'negative': '#DC143C',
        'neutral': '#4682B4'
    }
}
```

### Add New Airlines
Update the airlines configuration:
```python
AIRLINES = {
    'airindia': 'Air India',
    'spicejet': 'SpiceJet',
    'jetairways': 'Jet Airways',
    'indigo': 'IndiGo',
    'vistara': 'Vistara',
    'newairline': 'New Airline'  # Add your airline
}
```

## 📱 Mobile Access

The dashboard is responsive and works on mobile devices:
- Access via your computer's IP address
- Use `streamlit run app.py --server.address 0.0.0.0`

## 🔄 Data Updates

To update the data:
1. Replace `sentiment_analyzed_data.csv` with new data
2. Restart the Streamlit app
3. Data will be automatically refreshed

## 📈 Performance Tips

- **Large datasets**: Use date filters to reduce data size
- **Slow loading**: Enable caching in config.py
- **Memory issues**: Reduce max_rows in DATA_CONFIG

## 🆘 Need Help?

1. **Run the test suite**: `python test_app.py`
2. **Check logs**: Look for error messages in the terminal
3. **Verify data**: Ensure CSV format is correct
4. **Update dependencies**: `pip install --upgrade -r requirements.txt`

## 🎉 Success!

You should now see a beautiful, interactive dashboard with:
- ✈️ Real-time sentiment analysis
- 📊 Interactive visualizations
- 🗺️ Geographic mapping
- 📈 Trend analysis
- 🔍 Advanced filtering

Happy analyzing! 🚀 