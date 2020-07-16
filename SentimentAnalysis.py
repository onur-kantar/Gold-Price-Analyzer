from textblob import TextBlob

def analysis (texts):
    blob = TextBlob(texts)
    
    if blob.sentiment.polarity > 0: # Olumlu
        print(blob.sentiment)
        return 0
    else:                           # Olumsuz
        print(blob.sentiment)
        return 1    

    