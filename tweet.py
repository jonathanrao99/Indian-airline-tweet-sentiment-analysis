import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Load the dataset from CSV
data = pd.read_csv('indianairline.csv')  

# Load the sentiment analysis model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

# Define the labels for sentiment classes
labels = ['Negative', 'Neutral', 'Positive']

# Function to perform sentiment analysis on a single tweet
def analyze_sentiment(tweet):
    tweet_words = []
    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)
    tweet_proc = " ".join(tweet_words)
    
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    
    # Get the index of the sentiment class with the highest score
    sentiment_index = scores.argmax()
    return labels[sentiment_index]

# Apply sentiment analysis to each tweet in the dataset and add the predicted sentiment to a new column
count = 0
for i, tweet in enumerate(data['tweet_content']):
    data.at[i, 'Predicted_Sentiment'] = analyze_sentiment(tweet)
    count += 1
    print(f"Processed {count} tweets.", end='\r')

# Save the modified dataset with predicted sentiments to a new CSV file
data.to_csv('sentiment_analyzed_data.csv', index=False)  # Change 'sentiment_analyzed_data.csv' to your desired output file path

# Print message indicating sentiment analysis is complete
print("\nSentiment analysis has been successfully performed on all tweets.")

# Print count to indicate the progress of sentiment analysis
print(f"Total tweets processed: {count}")
