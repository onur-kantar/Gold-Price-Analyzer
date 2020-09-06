from selenium import webdriver
import time
import numpy as np 
import WriteToCSV as wts
import chromedriver_autoinstaller
import SentimentAnalysis as sm
import pandas as pd
from datetime import datetime, date

def scrape () :
    url1 = 'https://www.investing.com/currencies/xau-usd-historical-data'
    #url1 = 'https://www.investing.com/indices/usdollar-historical-data'
    url2 = 'https://www.gold.org/goldhub/data/gold-prices'
    chromedriver_autoinstaller.install()
    browser = webdriver.Chrome()
    browser.get(url1)
    browser.maximize_window()
    time.sleep(5)
    
    '''
    newYear = date(date.today().year, 1, 1)
    newYear = newYear.strftime('%m/%d/%Y')
    print(newYear)'''
    
    startDateName = date(2018,7,11)
    startDateName = startDateName.strftime('%m/%d/%Y')
    endDateName = date(2020,7,11)
    endDateName = endDateName.strftime('%m/%d/%Y')

    
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
    df['Date'] =  pd.to_datetime(df['Date'], format='%b %d, %Y').dt.date
    '''

    HighestOfYear = df["High"].max()
    LowestOfYear = df["Low"].min()

    mask = (df['Date'] > startDate) & (df['Date'] <= endDate)
    df = df.loc[mask].reset_index(drop=True)
    '''

    '''df['HighestOfYear'] = HighestOfYear
    df['LowestOfYear'] = LowestOfYear   '''
    
    
    classes = []
    classes = np.where(df['Open'] < df['Price'], '1', (np.where(df['Open'] > df['Price'], '-1', '0')))
    df['Target'] = classes
    
    df = df.drop(['Change %'], axis=1)
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

    df.to_csv('2.csv', index = False)
    xau = pd.read_csv('XAU.csv', encoding = 'UTF-8', delimiter=',')
    
    frames = [xau, df]
    result = pd.concat(frames, axis = 1)

    result.to_csv('2.csv', index = False)

    print(df) 
    











