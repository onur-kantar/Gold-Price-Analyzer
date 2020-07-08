import pandas as pd                     
import Preprocessing
import ScrapeTweets as st
import os
import CsvMerger as cm

twitterURL = 'https://twitter.com/search?f=live&q=(%23XAUUSD)%20lang%3Aen%20-filter%3Areplies&src=typed_query'
pageSize = 2000
csvPath = os.getcwd()+"\\data.csv"
filePath = os.getcwd()
st.scrape(twitterURL, pageSize, csvPath)

"""
cm.merge(filePath)

df = pd.read_csv('merged.csv', encoding = 'UTF-8', sep=',')

x = df.iloc[:,0]

x = Preprocessing.series(x)

print(pd.DataFrame(x))"""

