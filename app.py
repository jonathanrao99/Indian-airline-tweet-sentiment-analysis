import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import numpy as np

#title
st.title('Tweet Sentiment Analysis')
#markdown
st.markdown('This application is all about tweet sentiment analysis of airlines. We can analyse reviews of the passengers using this streamlit app.')
#sidebar
st.sidebar.title('Sentiment analysis of airlines')
# sidebar markdown
st.sidebar.markdown("🛫We can analyse passengers review from this application.🛫")
#loading the data (the csv file is in the same folder)
#if the file is stored the copy the path and paste in read_csv method.
data = pd.read_csv('sentiment_analyzed_data.csv', encoding='latin-1')
#checkbox to show data
if st.checkbox("Show Data"):
    required_columns = ['date','tweet_location','user','tweet_content','Airline', 'Predicted_Sentiment']  # Select required columns
    st.write(data[required_columns].head(50))
#subheader
st.sidebar.subheader('Tweets Analyser')
#radio buttons
tweets=st.sidebar.radio('Sentiment Type',('Positive','Negative','Neutral'))
st.write(data.query('Predicted_Sentiment==@tweets')[['tweet_content']].sample(1).iat[0,0])
st.write(data.query('Predicted_Sentiment==@tweets')[['tweet_content']].sample(1).iat[0,0])
st.write(data.query('Predicted_Sentiment==@tweets')[['tweet_content']].sample(1).iat[0,0])

#selectbox + visualisation
# An optional string to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content.
## Multiple widgets of the same type may not share the same key.
select=st.sidebar.selectbox('Visualisation Of Tweets',['Histogram','Pie Chart'],key=1)
sentiment=data['Predicted_Sentiment'].value_counts()
sentiment=pd.DataFrame({'Sentiment':sentiment.index,'Tweets':sentiment.values})
st.markdown("###  Sentiment count")
if select == "Histogram":
        fig = px.bar(sentiment, x='Sentiment', y='Tweets', color = 'Tweets', height= 500)
        st.plotly_chart(fig)
else:
        fig = px.pie(sentiment, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)


st.sidebar.markdown('Time & Location of tweets')
hr = st.sidebar.slider("Hour of the day", 0, 23)

# Filter data for the selected hour
data['Date'] = pd.to_datetime(data['date'])
hourly_data = data[data['Date'].dt.hour == hr]

# Display map
st.markdown("### Location of the tweets based on the hour of the day")
st.markdown("%i tweets during %i:00 and %i:00" % (len(hourly_data), hr, (hr+1) % 24))
st.map(hourly_data)

#multiselect
st.sidebar.subheader("Airline tweets by sentiment")
choice = st.sidebar.multiselect("Airlines", ('AirIndia', 'Spicejet', 'Jetairways', 'Indigo', 'Vistara'))
if len(choice) > 0:
    air_data = data[data.Airline.isin(choice)]
    
    # Sentiment Comparison
    comparison_data = air_data.groupby(['Airline', 'Predicted_Sentiment']).size().unstack(fill_value=0)
    fig_comparison = px.bar(comparison_data, x=comparison_data.index, y=['Positive', 'Negative', 'Neutral'], title='Sentiment Comparison')
    st.plotly_chart(fig_comparison)


# Sentiment Analysis Breakdown
if len(choice) > 0:
    breakdown_data = air_data.groupby(['Airline', 'Predicted_Sentiment']).size().unstack(fill_value=0)
    breakdown_data['Total'] = breakdown_data.sum(axis=1)
    breakdown_data['Positive (%)'] = (breakdown_data['Positive'] / breakdown_data['Total']) * 100
    breakdown_data['Negative (%)'] = (breakdown_data['Negative'] / breakdown_data['Total']) * 100
    breakdown_data['Neutral (%)'] = (breakdown_data['Neutral'] / breakdown_data['Total']) * 100
    st.write(breakdown_data)
