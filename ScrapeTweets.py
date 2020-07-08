from selenium import webdriver
import time
import numpy as np 
import WriteToCSV as wts
import chromedriver_autoinstaller

def scrape (twitterURL, pageSize, csvPath, firstPageSize = 1):
    chromedriver_autoinstaller.install()
    browser = webdriver.Chrome()
    browser.get(twitterURL)
    tweets = []
    time.sleep(5)
    lenOfPage = 0;

    for i in range(1, int(firstPageSize)):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;")
        print('Sayfa Sayısı : ' + str(i) + ' / ' + str(firstPageSize) + '\n')
        time.sleep(2)

    for j in range(1, int(pageSize+1)):
        try:
            elements = browser.find_elements_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div")
            time.sleep(2)
            for element in elements:
                tweets.append(element.text)
        except:
            elements = browser.find_elements_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div/div/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div")
            time.sleep(2)
            for element in elements:
                tweets.append(element.text)
           
        lastCount = lenOfPage
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        
        print(str(j)+ ' / ' + str(pageSize))
        time.sleep(2)

        if lastCount == lenOfPage:
            print('Sayfa Sınırına Ulaşıldı!')
            browser.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            myLenOfPage = browser.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == myLenOfPage:
                print('tükendik')
                #browser.close()
                break;
                
    wts.writeRow(csvPath, np.unique(tweets))
    print('Başarıyla Tamamlandı')
    #browser.close()

