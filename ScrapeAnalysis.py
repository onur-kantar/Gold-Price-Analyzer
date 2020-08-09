from selenium import webdriver
import time
import numpy as np 
import WriteToCSV as wts
import chromedriver_autoinstaller
import SentimentAnalysis as sm
import pandas as pd
from datetime import datetime, date

def scrape () :
    #url1 = 'https://www.investing.com/currencies/xau-usd-historical-data'
    url1 = 'https://www.investing.com/indices/usdollar-historical-data'
    url2 = 'https://www.gold.org/goldhub/data/gold-prices'
    chromedriver_autoinstaller.install()
    browser = webdriver.Chrome()
    browser.get(url1)
    browser.maximize_window()
    time.sleep(5)
    
    newYear = date(date.today().year, 1, 1)
    newYear = newYear.strftime('%m/%d/%Y')
    print(newYear)
    
    calendar = browser.find_element_by_id('flatDatePickerCanvasHol')
    calendar.click()
    time.sleep(1)

    startDate = browser.find_element_by_id('startDate')
    startDate.clear()
    startDate.send_keys(newYear)
    time.sleep(1)

    calendar = browser.find_element_by_id('applyBtn')
    calendar.click()
    time.sleep(1)

    df = pd.read_html(browser.page_source)[0]
    
    df['Date'] =  pd.to_datetime(df['Date'], format='%b %d, %Y').dt.date

    startDate = date(2020,2,11)
    endDate= date(2020,7,12)
    HighestOfYear = df["High"].max()
    LowestOfYear = df["Low"].min()

    mask = (df['Date'] > startDate) & (df['Date'] <= endDate)
    df = df.loc[mask].reset_index(drop=True)

    df['HighestOfYear'] = HighestOfYear
    df['LowestOfYear'] = LowestOfYear   
    
    classes = []
    classes = np.where(df['Open'] < df['Price'], '1', (np.where(df['Open'] > df['Price'], '-1', '0')))
    df['target'] = classes
    
    df = df.drop(['Vol.'], axis=1)
    df = df.drop(['Date'], axis=1)

    #df = df.drop(['Change %'], axis=1)
    df = df.rename(columns={'Price': 'Close'})
    df = df.rename(columns={'Close': 'DXY_Close'})
    df = df.rename(columns={'Open': 'DXY_Open'})
    df = df.rename(columns={'High': 'DXY_High'})
    df = df.rename(columns={'low': 'DXY_Low'})
    df = df.rename(columns={'HighestOfYear': 'DXY_HighestOfYear'})
    df = df.rename(columns={'LowestOfYear': 'DXY_LowestOfYear'})
    df = df.rename(columns={'target': 'DXY_Target'})

    df.to_csv('DXY.csv', index = False)
    xau = pd.read_csv('XAU.csv', encoding = 'UTF-8', delimiter=',')
    
    frames = [xau, df]
    result = pd.concat(frames, axis = 1)

    result.to_csv('XAU_DXY.csv', index = False)

    print(result) 
    











