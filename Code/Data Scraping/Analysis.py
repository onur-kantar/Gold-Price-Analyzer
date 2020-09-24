from textblob import TextBlob
import numpy as np 

def tweetAnalysis (texts):
    blob = TextBlob(texts)
    
    if blob.sentiment.polarity > 0: # Olumlu
        print(blob.sentiment)
        return 1
    else:                           # Olumsuz
        print(blob.sentiment)
        return 0   

def numericalAnalysis (numerical):
    return np.where(numerical['Open'] < numerical['Price'], 1, 0)
