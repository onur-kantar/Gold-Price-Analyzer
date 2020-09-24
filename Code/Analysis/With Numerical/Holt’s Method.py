import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from statsmodels.tsa.api import Holt
from statsmodels.tsa.stattools import acf

df = pd.read_csv("/content/drive/My Drive/Colab Notebooks/Gold Price Analysis/DS/XAU_1_Weekend.csv",encoding = 'UTF-8', sep=',')
df = df.drop(['Open', 
              'High', 
              'Low',
              'Target'
              ], axis=1)

df['Date']=pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df = df.sort_index()

df.plot(figsize=(15, 6))
plt.show()

startDate = date(2019,7,11)
endDate = date(2020,7,11)

data = df.Price.values
index= df.index.values
series = pd.Series(data, index)


fit = Holt(series, damped=True).fit(smoothing_level=0.8, smoothing_slope=0.2)
fcast = fit.predict(startDate, endDate).rename(r'$\alpha=%s$'%fit.model.params['smoothing_level'])

fig, ax = plt.subplots(figsize=(16,8))
series.plot(kind='line', color='dodgerblue', ax=ax, label='Gerçek Değer', legend=True)  #expected
fcast.plot(kind='line', color='darkorange', ax=ax, label='Tahmin Edilen Değer', legend=True) #predicted
plt.title("Holt's Yöntemi İle Altın Fiyat Tahmini")
plt.xlabel("Tarih")
plt.ylabel("Altının Fiyatı")
plt.show()


def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
    me = np.mean(forecast - actual)             # ME
    mae = np.mean(np.abs(forecast - actual))    # MAE
    mpe = np.mean((forecast - actual)/actual)   # MPE
    rmse = np.mean((forecast - actual)**2)**.5  # RMSE
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    mins = np.amin(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    minmax = 1 - np.mean(mins/maxs)             # minmax
    acf1 = acf(forecast-actual)[1]                      # ACF1
    return({'mape':mape, 'me':me, 'mae': mae, 
            'mpe': mpe, 'rmse':rmse, 'acf1':acf1, 
            'corr':corr, 'minmax':minmax})

fa = forecast_accuracy(fcast, series)

fa_df = pd.DataFrame(fa,index=[0])
print(fa_df)