from textblob import TextBlob

def analysis (texts):
    blob = TextBlob(texts)
    
    if blob.sentiment.polarity > 0: # Olumlu
        return 1    
    if blob.sentiment.polarity < 0: # Olumsuz
        return 2    
    else:                           # Nötr
        return 0
    