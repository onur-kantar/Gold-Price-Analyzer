import re
import pandas as pd                     

def hight(sentence):
        
    # URL Silme İşlemi
    sentence = re.sub(r'http\S+', '', sentence)
    
    # Hashtag Silme İşlemi
    sentence = re.sub(r'#\S+', '', sentence)
    
    # Etkiket Silme İşlemi
    sentence = re.sub(r'@\S+', '', sentence)
    
    # E-Mail Adresi Silme İşlemi
    sentence = re.sub(r'\S+@\S+', '', sentence)

    # Sayı Silme İşlemi
    sentence = re.sub(r'[\d\s]', ' ', sentence)

    # Noktalama İşareti Silme İşlemi
    sentence = re.sub(r'[^\w\s]', ' ', sentence)
    
    # A'dan Z'ye Olmayan Harfleri Silme İşlemi
    sentence = re.sub(r'[^a-zA-Z\s]', ' ', sentence)
    
    # Tek Karakter Silme İşlemi
    sentence = re.sub(r'\b[a-zA-Z]\b', '', sentence)
    
    # Birden Çok Boşluğu Silme İşlemi
    sentence = re.sub(r'\s+', ' ', sentence)
    
    # Baştaki ve Sondaki Boşukları Silme İşlemi
    sentence = sentence.strip()
    
    # Tüm Harfleri Küçük Harfe Çevirme İşlemi
    sentence = sentence.lower()
    
    if sentence == '' or sentence == ' ':
        # Boş Değerleri NaN Olarak Döndürme İşlemi
        return float('nan')
    else:
        return sentence

def medium(sentence):
        
    # URL Silme İşlemi
    sentence = re.sub(r'http\S+', '', sentence)
    
    # Hashtag Silme İşlemi
    sentence = re.sub(r'#\S+', '', sentence)
    
    # Etkiket Silme İşlemi
    sentence = re.sub(r'@\S+', '', sentence)
    
    # E-Mail Adresi Silme İşlemi
    sentence = re.sub(r'\S+@\S+', '', sentence)
    
    # A'dan Z'ye Olmayan Harfleri Silme İşlemi
    sentence = re.sub(r'[^a-zA-Z0-9\s]', ' ', sentence)
    
    # Birden Çok Boşluğu Silme İşlemi
    sentence = re.sub(r'\s+', ' ', sentence)
    
    # Baştaki ve Sondaki Boşukları Silme İşlemi
    sentence = sentence.strip()
    
    # Tüm Harfleri Küçük Harfe Çevirme İşlemi
    sentence = sentence.lower()
    
    if sentence == '' or sentence == ' ':
        # Boş Değerleri NaN Olarak Döndürme İşlemi
        return float('nan')
    else:
        return sentence

def low(sentence):
    
    # Birden Çok Boşluğu Silme İşlemi
    sentence = re.sub(r'\s+', ' ', sentence)
    
    # Baştaki ve Sondaki Boşukları Silme İşlemi
    sentence = sentence.strip()
    
    # Virgülleri Kaldırma İşlemi
    sentence = sentence.replace(',', '')

    # Tüm Harfleri Küçük Harfe Çevirme İşlemi
    sentence = sentence.lower()
    
    if sentence == '' or sentence == ' ':
        # Boş Değerleri NaN Olarak Döndürme İşlemi
        return float('nan')
    else:
        return sentence
    
def clean(series, process_type = 'medium'):
    series = pd.Series(series)
    if process_type == 'hight':
        series = series.apply(hight)
    elif process_type == 'low':
        series = series.apply(low)
    elif process_type == 'medium':
        series = series.apply(medium)
    series = series.dropna()
    series = series.drop_duplicates()
    series = series.reset_index(drop=True)
    return series

