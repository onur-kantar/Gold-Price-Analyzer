from selenium import webdriver
import time
import numpy as np 
import chromedriver_autoinstaller
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def ScrapeTweet (twitterURL, minTweetSize):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(twitterURL)
    time.sleep(5)
    tweets = []
    lenOfPage = 0;

    while True:
        try:
            elements = browser.find_elements_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div")
            time.sleep(2)
            for element in elements:
                tweets.append(element.text)
            print(tweets)
        except:
            print('Bir Hata İle Karşılaşıldı Fakat Devam Ediliyor')
            continue
            
        print(str(len(tweets))+ ' / ' + str(minTweetSize))
        time.sleep(2)
        
        if len(tweets) >= int(minTweetSize):
            print('İstenilen Tweet Sayısı Aşıldı')
            newSize = int(input('Daha Fazla Kazımak İstiyorsanız Değer Giriniz? (0 = Bitir): '))
            if newSize > 0:
                minTweetSize = minTweetSize + newSize
                print('Devam Ediliyor. Yeni Hedef: ' + str(minTweetSize))
            else:
                print('Başarıyla Tamamlandı')
                return tweets

        lastCount = lenOfPage
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

        while lastCount == lenOfPage:
            print('Sayfa Sınırına Ulaşıldı!')
            browser.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            myLenOfPage = browser.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == myLenOfPage:
                print('Sayfa Sınırına Ulaşıldığı Düşünülüyor')
                decision = input('Bitirmek İstiyor Musunuz? (0 = Bitir): ')
                if decision != '0':
                    print('Devam Etmeye Çalışılınıyor')
                    continue
                else:
                    print('Başarıyla Tamamlandı')
                    return tweets
            else:
                break

    print('Başarıyla Tamamlandı')
    return tweets

def ScrapeNumerical (url, startDateName, endDateName) :
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    time.sleep(5)
        
    calendar = browser.find_element_by_id('flatDatePickerCanvasHol')
    calendar.click()
    time.sleep(1)

    startDate = browser.find_element_by_id('startDate')
    startDate.clear()
    startDate.send_keys(startDateName)
    time.sleep(1)
    
    endDate = browser.find_element_by_id('endDate')
    endDate.clear()
    endDate.send_keys(endDateName)
    time.sleep(1)

    calendar = browser.find_element_by_id('applyBtn')
    calendar.click()
    time.sleep(1)

    df = pd.read_html(browser.page_source)[0]
    
    print('Başarıyla Tamamlandı')

    return df;
# =============================================================================
# 
#     df['Date'] =  pd.to_datetime(df['Date'], format='%b %d, %Y').dt.date
#     
#     df.to_csv('2.csv', index = False)
# 
#     classes = []
#     classes = np.where(df['Open'] < df['Price'], '1', (np.where(df['Open'] > df['Price'], '-1', '0')))
#     df['Target'] = classes
# =============================================================================
    