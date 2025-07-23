# ✈️ SkySentiment - Indian Airline Tweet Sentiment Analysis

A comprehensive real-time sentiment analysis platform for Indian airline conversations on Twitter. This advanced dashboard provides deep insights into public perception, trends, and performance metrics across major Indian airlines.

## 🚀 Features

### 📊 **Enhanced Dashboard**
- **Modern UI/UX** with responsive design and intuitive navigation
- **Multi-tab interface** for organized data exploration
- **Real-time metrics** and KPIs with interactive visualizations
- **Advanced filtering** capabilities for precise data analysis

### 📈 **Advanced Analytics**
- **Temporal Trend Analysis** - Track sentiment changes over time
- **Geographic Visualization** - Interactive maps showing tweet locations
- **Airline Performance Comparison** - Detailed competitive analysis
- **Content Analysis** - Word clouds, hashtag analysis, and text insights
- **Engagement Metrics** - Retweet and like analysis by sentiment

### 🎯 **Key Capabilities**
- **Real-time Data Processing** with caching for optimal performance
- **Interactive Visualizations** using Plotly and Folium
- **Advanced Filtering** by date range, airline, and sentiment
- **Export Functionality** for filtered data analysis
- **Confidence Scoring** for sentiment prediction accuracy

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Indian-airline-tweet-sentiment-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**
   Open your browser and navigate to `http://localhost:8501`

## 📋 Data Requirements

The application expects a CSV file named `sentiment_analyzed_data.csv` with the following columns:

- `date`: Tweet timestamp
- `user`: Twitter username
- `tweet_content`: Tweet text content
- `Airline`: Airline name (airindia, spicejet, jetairways, indigo, vistara)
- `Predicted_Sentiment`: Sentiment classification (Positive, Negative, Neutral)
- `Sentiment_Confidence`: Confidence score (0-1)
- `tweet_location`: Geographic location
- `latitude`, `longitude`: Geographic coordinates
- `retweet_count`, `like_count`: Engagement metrics

## 🎨 Dashboard Sections

### 1. **Overview Tab** 📊
- Executive summary with key metrics
- Sentiment distribution charts
- Airline performance overview
- Real-time KPIs

### 2. **Trends & Analytics Tab** 📈
- Temporal sentiment trends
- Hourly activity patterns
- Weekly sentiment distribution
- Confidence analysis
- Engagement metrics

### 3. **Geographic Analysis Tab** 🗺️
- Interactive map visualization
- Geographic insights
- Location-based sentiment analysis
- Top tweet locations

### 4. **Airline Comparison Tab** 🏢
- Performance metrics table
- Sentiment distribution comparison
- Positive sentiment ranking
- Engagement comparison

### 5. **Content Analysis Tab** 📝
- Word cloud visualizations
- Hashtag analysis
- Tweet length distribution
- Content insights by sentiment

### 6. **Deep Dive Tab** 🔍
- Sample tweet exploration
- Advanced filtering options
- Raw data access
- Export functionality

## 🔧 Configuration

### Customization Options
- **Date Range Filtering**: Analyze specific time periods
- **Airline Selection**: Focus on specific airlines
- **Sentiment Filtering**: Filter by sentiment type
- **Confidence Thresholds**: Set minimum confidence scores
- **Engagement Filters**: Filter by retweet/like counts

### Performance Optimization
- **Data Caching**: Automatic caching for improved performance
- **Lazy Loading**: Efficient data processing
- **Memory Management**: Optimized for large datasets

## 📊 Key Metrics

### Sentiment Analysis
- **Positive Sentiment Percentage**: Overall positive sentiment rate
- **Negative Sentiment Percentage**: Overall negative sentiment rate
- **Confidence Scores**: Prediction accuracy metrics
- **Sentiment Trends**: Temporal sentiment changes

### Engagement Analysis
- **Retweet Analysis**: Viral content identification
- **Like Analysis**: Popular content metrics
- **Engagement Rates**: Overall interaction metrics
- **Viral Tweet Identification**: High-engagement content

### Geographic Insights
- **Location Distribution**: Tweet geographic spread
- **Regional Sentiment**: Location-based sentiment analysis
- **Hotspot Identification**: High-activity areas

## 🚀 Advanced Features

### Real-time Analytics
- **Live Data Processing**: Real-time sentiment analysis
- **Dynamic Updates**: Automatic data refresh
- **Performance Monitoring**: System health metrics

### Export Capabilities
- **CSV Export**: Filtered data export
- **Chart Export**: Visualization downloads
- **Report Generation**: Automated reporting

### API Integration Ready
- **Modular Design**: Easy API integration
- **Data Pipeline**: Scalable data processing
- **Extensible Architecture**: Future feature additions

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Data Sources**: Twitter API and public datasets
- **Visualization Libraries**: Plotly, Folium, Matplotlib
- **Framework**: Streamlit for rapid web app development
- **Community**: Open source contributors and aviation enthusiasts

## 📞 Support

For support, questions, or feature requests:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**✈️ SkySentiment Dashboard** | *Empowering data-driven insights in Indian aviation*
