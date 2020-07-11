from selenium import webdriver
import time
import numpy as np 
import WriteToCSV as wts
import chromedriver_autoinstaller
import SentimentAnalysis as sm
import pandas as pd

def scrape (twitterURL, minTweetSize):
    chromedriver_autoinstaller.install()
    browser = webdriver.Chrome()
    browser.get(twitterURL)
    time.sleep(5)
    tweets = []
    lenOfPage = 0;

    while True:
        try:
            elements = browser.find_elements_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div")
            time.sleep(2)
            for element in elements:
                tweets.append(element.text)
        except:
            continue
            '''
            elements = browser.find_elements_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div")
            time.sleep(2)
            for element in elements:
                tweets.append(element.text)
            '''
            
        print(str(len(tweets))+ ' / ' + str(minTweetSize))
        time.sleep(2)
        
        if len(tweets) > int(minTweetSize):
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
         
    #wts.writeRow(csvPath, np.unique(tweets))
    #browser.close()

