import pandas as pd                     
import Preprocessing as pre
import ScrapeTweets as st
import os
import CsvMerger as cm
import SentimentAnalysis as sa
import numpy as numpy
import WriteToCSV as wcsv
import Augmenter as aug
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
        'target' : classes
    }
wcsv.writeRow('gold_price.csv', dict_val)
#-------------------------------------------------

df = pd.read_csv('augment_gold_price.csv', encoding = 'UTF-8', delimiter=',')
print(df)

x = df['tweet']
y = df['target']
import seaborn as sns
sns.countplot(y)
# Sampling ----------------------------------------

# Class count
count_class_1, count_class_0 = df.target.value_counts()

# Divide by class
df_class_0 = df[df['target'] == 0]
df_class_1 = df[df['target'] == 1]

# Random Under-Sampling 

df_class_1_under = df_class_1.sample(count_class_0)
df_under = pd.concat([df_class_1_under, df_class_0], axis=0)

df_under.target.value_counts().plot(kind='bar', title='Count (target)');

# Random Over-Sampling 

df_class_0_over = df_class_0.sample(count_class_1, replace=True)
df_over = pd.concat([df_class_0_over, df_class_1], axis=0)

df_over.target.value_counts().plot(kind='bar', title='Count (target)');

#-------------------------------------------------

newdf = aug.augments(x, y)
wcsv.writeRow('augment_gold_price.csv', dict_val)

print(newdf)




















