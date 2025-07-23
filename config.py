# Configuration file for SkySentiment Dashboard

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'page_title': 'SkySentiment - Indian Airline Tweet Analysis',
    'page_icon': '✈️',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Data Configuration
DATA_CONFIG = {
    'csv_file': 'sentiment_analyzed_data.csv',
    'encoding': 'latin-1',
    'cache_ttl': 3600,  # Cache time in seconds
    'max_rows': 10000   # Maximum rows to load for performance
}

# Visualization Configuration
VIZ_CONFIG = {
    'color_scheme': {
        'positive': '#2E8B57',
        'negative': '#DC143C',
        'neutral': '#4682B4',
        'primary': '#1f77b4',
        'secondary': '#ff7f0e'
    },
    'chart_height': 400,
    'wordcloud_max_words': 100,
    'map_zoom': 5,
    'map_tiles': 'OpenStreetMap'
}

# Filter Configuration
FILTER_CONFIG = {
    'default_date_range_days': 30,
    'min_confidence_threshold': 0.0,
    'max_tweets_per_page': 50,
    'geographic_limit': 100  # Max tweets to show on map
}

# Airline Configuration
AIRLINES = {
    'airindia': 'Air India',
    'spicejet': 'SpiceJet',
    'jetairways': 'Jet Airways',
    'indigo': 'IndiGo',
    'vistara': 'Vistara'
}

# Sentiment Configuration
SENTIMENTS = {
    'positive': 'Positive',
    'negative': 'Negative',
    'neutral': 'Neutral'
}

# Geographic Configuration
GEO_CONFIG = {
    'default_lat': 20.5937,  # India center latitude
    'default_lon': 78.9629,  # India center longitude
    'location_mapping': {
        'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
        'Delhi': {'lat': 28.7041, 'lon': 77.1025},
        'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
        'Chennai': {'lat': 13.0827, 'lon': 80.2707},
        'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
        'Kolkata': {'lat': 22.5726, 'lon': 88.3639}
    }
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'enable_caching': True,
    'cache_clear_interval': 3600,  # Clear cache every hour
    'max_memory_usage': 0.8,  # 80% of available memory
    'chunk_size': 1000  # Process data in chunks
}

# Export Configuration
EXPORT_CONFIG = {
    'supported_formats': ['csv', 'json'],
    'max_export_rows': 10000,
    'include_metadata': True,
    'filename_prefix': 'skysentiment_export'
}

# UI Configuration
UI_CONFIG = {
    'theme': {
        'primary_color': '#1f77b4',
        'secondary_color': '#ff7f0e',
        'background_color': '#f0f2f6',
        'text_color': '#333333'
    },
    'layout': {
        'sidebar_width': 300,
        'main_padding': 20,
        'card_padding': 15
    },
    'animations': {
        'enable_chart_animations': True,
        'enable_page_transitions': True
    }
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    'enable_tracking': False,
    'tracking_id': None,
    'custom_events': [
        'filter_applied',
        'export_downloaded',
        'chart_interaction',
        'tab_switched'
    ]
}

# Security Configuration
SECURITY_CONFIG = {
    'enable_authentication': False,
    'allowed_file_types': ['.csv', '.json'],
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'sanitize_inputs': True
} 