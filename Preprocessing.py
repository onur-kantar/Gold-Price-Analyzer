import re

def sentence(sentence):
        
    # URL Silme İşlemi
    sentence = re.sub('http\S+', '', sentence)
    
    # Hashtag Silme İşlemi
    sentence = re.sub('#\S+', '', sentence)
    
    # Etkiket Silme İşlemi
    sentence = re.sub('@\S+', '', sentence)
    
    # E-Mail Adresi Silme İşlemi
    sentence = re.sub('\S+@\S+', '', sentence)

    # Sayı Silme İşlemi
    sentence = re.sub('[\d\s]', ' ', sentence)

    # Noktalama İşareti Silme İşlemi
    sentence = re.sub('[^\w\s]', ' ', sentence)
    
    # Tek Karakter Silme İşlemi
    sentence = re.sub("\b[\w\s]\b", ' ', sentence)
    
    # Birden Çok Boşluğu Silme İşlemi
    sentence = re.sub('\s+', ' ', sentence)
    
    # A'dan Z'ye Olmayan Harfleri Silme İşlemi
    sentence = re.sub('[^a-zA-Z\s]', ' ', sentence)
    
    # Baştaki ve Sondaki Boşukları Silme İşlemi
    sentence = sentence.strip()
    
    # Tüm Harfleri Küçük Harfe Çevirme İşlemi
    sentence = sentence.lower()
    
    if sentence == '' or sentence == ' ':
        # Boş Değerleri NaN Olarak Döndürme İşlemi
        return float('nan')
    else:
        return sentence

def series(series):
    series = series.apply(sentence)
    series = series.dropna()
    series = series.drop_duplicates()
    series = series.reset_index(drop=True)
    return series