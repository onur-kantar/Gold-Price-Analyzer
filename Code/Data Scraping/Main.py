import pandas as pd                     
import Preprocessing as pre
import Scrape
import Analysis 
import WriteToCSV as wcsv
import Augmenter as aug


# Tweet Kazıma ------------------------------------ 
url = 'https://twitter.com/search?f=live&q=(%23XAUUSD)%20lang%3Aen%20-filter%3Areplies&src=typed_query'
minTweetSize = 100
tweets = Scrape.ScrapeTweet(url, minTweetSize)
#-------------------------------------------------

# Temizleme İşlemi -------------------------------
tweets = pre.tweetClean(tweets, 'medium')
#-------------------------------------------------        
                                                                                                              
# Etiketleme İşlemi ------------------------------
classes = []
classes = tweets.apply(Analysis.tweetAnalysis)
#-------------------------------------------------

# .csv Dosyasına Yazdırma İşlemi -----------------
dict_val = {
        'tweet' : tweets,
        'target' : classes
    }
df_tweets = pd.DataFrame(dict_val)
wcsv.writeRow('tweets.csv', dict_val)
#-------------------------------------------------

# Sampling ---------------------------------------

# Class count
count_class_1, count_class_0 = df_tweets.target.value_counts()

# Divide by class
df_class_0 = df_tweets[df_tweets['target'] == 0]
df_class_1 = df_tweets[df_tweets['target'] == 1]

# Random Under-Sampling 

df_class_1_under = df_class_1.sample(count_class_0)
df_under = pd.concat([df_class_1_under, df_class_0], axis=0)
wcsv.writeRow('twitter_under_sampling.csv', df_under)

# Random Over-Sampling 

df_class_0_over = df_class_0.sample(count_class_1, replace=True)
df_over = pd.concat([df_class_0_over, df_class_1], axis=0)
wcsv.writeRow('twitter_over_sampling.csv', df_over)

# Augmenter  

df_augment = aug.augments(df_tweets['tweet'], df_tweets['target'])
wcsv.writeRow('augment_twitter.csv', df_augment)

#-------------------------------------------------

# =============================================================================

# Sayısal Veri Kazıma ----------------------------
url = input("Verilerini Toplamak İstediğiniz Yatırım Aracının " +
            "Investing'deki Geçmiş Verileri Sayfasının URL'sini Girin. " +
            "Örn: https://www.investing.com/currencies/xau-usd-historical-data: ")
    
startDateName = input("Başlangıç Tarihi Girin. Örn: 7/13/2018: ");
endDateName = input("Başlangıç Tarihi Girin. Örn: 7/13/2020: ");
numerical = Scrape.ScrapeNumerical(url, startDateName, endDateName)
#-------------------------------------------------
print(numerical)
# Temizleme İşlemi -------------------------------
numerical = pre.numericalClean(numerical)
#-------------------------------------------------        
                                                                                                              
# Etiketleme İşlemi ------------------------------
classes = []
classes = Analysis.numericalAnalysis(numerical)
#-------------------------------------------------

# .csv Dosyasına Yazdırma İşlemi -----------------
numerical['target'] = classes
wcsv.writeRow('tweetas.csv', numerical)
#-------------------------------------------------

# Sampling ---------------------------------------

# Class count
count_class_1, count_class_0 = numerical.target.value_counts()

# Divide by class
df_class_0 = numerical[numerical['target'] == 0]
df_class_1 = numerical[numerical['target'] == 1]

# Random Under-Sampling 

df_class_1_under = df_class_1.sample(count_class_0)
df_under = pd.concat([df_class_1_under, df_class_0], axis=0)
wcsv.writeRow('numerical_under_sampling.csv', df_under)

# Random Over-Sampling 

df_class_0_over = df_class_0.sample(count_class_1, replace=True)
df_over = pd.concat([df_class_0_over, df_class_1], axis=0)
wcsv.writeRow('numerical_over_sampling.csv', df_over)

#-------------------------------------------------