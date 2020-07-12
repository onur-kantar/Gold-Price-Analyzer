import pandas as pd                     
import Preprocessing as pre
import ScrapeTweets as st
import os
import CsvMerger as cm
import SentimentAnalysis as sa
import numpy as numpy
import WriteToCSV as wcsv

# Veri Kazıma ------------------------------------ birçok linkten çek
twitterURL = 'https://twitter.com/search?f=live&q=(%23XAUUSD)%20lang%3Aen%20-filter%3Areplies&src=typed_query'
minTweetSize = 30000
tweets = st.scrape(twitterURL, minTweetSize)
#-------------------------------------------------

# .csv Dosyasına Yazdırma İşlemi -----------------
dataSetPath = r'C:\Users\onur\Documents\GitHub\Gold-Analysis\Data Set'
dict_val = {
        'tweet' : tweets
    }
wcsv.writeRow('gold_tweets.csv', dict_val, dataSetPath)
#-------------------------------------------------


# .csv Dosyalarını Birleştirme İşlemi ------------
filePath = r'C:\Users\onur\Documents\GitHub\Gold-Analysis\Data Set'
cm.merge(filePath, 'gold_all.csv')
#-------------------------------------------------

# Veriyi Çekip Yazdırma İşlemi -------------------
df = pd.read_csv('gold_all.csv', encoding = 'UTF-8', delimiter=',')
x = df['tweet']
print(df)
#-------------------------------------------------

# Temizleme İşlemi -------------------------------
x = pre.clean(x, 'medium')
#-------------------------------------------------

# Etiketleme İşlemi ------------------------------
classes = []
classes = x.apply(sa.analysis)
#-------------------------------------------------

# .csv Dosyasına Yazdırma İşlemi -----------------
dict_val = {
        'tweet' : x,
        'class' : classes
    }
wcsv.writeRow('gold_price.csv', dict_val)
#-------------------------------------------------

df = pd.read_csv('gold_price.csv', encoding = 'UTF-8', delimiter=',')
print(df)
