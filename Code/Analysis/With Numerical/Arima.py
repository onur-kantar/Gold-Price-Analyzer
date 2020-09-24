import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import warnings
from pandas import datetime
from sklearn.metrics import mean_squared_error
import numpy
from math import sqrt

df = pd.read_csv("/content/drive/My Drive/Colab Notebooks/Gold Price Analysis/DS/XAU_1_Weekend.csv",encoding = 'UTF-8', sep=',')
df = df.drop(['Open', 
              'High', 
              'Low',
              'Target'
              ], axis=1)

df['Date']=pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df = df.sort_index()

# evaluate an ARIMA model for a given order (p,d,q)
def evaluate_arima_model(X, arima_order):
    # prepare training dataset
    train_size = int(len(X) * 0.66)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]
    # make predictions
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
    # calculate out of sample error
    error = mean_squared_error(test, predictions)
    return error
 
# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p,d,q)
                try:
                    mse = evaluate_arima_model(dataset, order)
                    if mse < best_score:
                        best_score, best_cfg = mse, order
                    print('ARIMA%s MSE=%.3f' % (order,mse))
                except:
                    continue
    print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))
 
# load dataset
def parser(x):
    return datetime.strptime('190'+x, '%Y-%m')
#series1 = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
# evaluate parameters
p_values = [0, 1, 2, 4, 6, 8, 10]
d_values = range(0, 3)
q_values = range(0, 3)
warnings.filterwarnings("ignore")
evaluate_models(df.values, p_values, d_values, q_values)

def difference(dataset):
    diff = list()
    for i in range(1, len(dataset)):
        value = dataset[i] - dataset[i - 1]
        diff.append(value)
    return numpy.array(diff)
def predict(coef, history):
    yhat = 0.0
    for i in range(1, len(coef)+1):
        yhat += coef[i-1] * history[-i]
    return yhat

X = df.values
size = int(len(X) * 0.33)
train, test = X[0:size], X[size:]
history = [x for x in train]
predictions = list()
history_size = len(history)

for t in range(len(X)):
    model = ARIMA(history, order=(10,1,0))
    model_fit = model.fit(trend='nc', disp=False)
    ar_coef, ma_coef = model_fit.arparams, model_fit.maparams
    resid = model_fit.resid
    diff = difference(history)
    yhat = history[-1] + predict(ar_coef, diff) + predict(ma_coef, resid)
    predictions.append(yhat)
    obs = X[t]
    history.append(obs)
    print('>predicted=%.3f, expected=%.3f' % (yhat, obs))

rmse = sqrt(mean_squared_error(X, predictions))
print('Test RMSE: %.3f' % rmse)
mape = np.mean(np.abs(predictions - X)/np.abs(X))  # MAPE
print('MAPE: %.3f'% mape)
print (t)

pred = []
for a in predictions:
  for b in a:
    b = round(b, 2)
    pred.append(b)
expec = []
for a in X:
  for b in a:
    b = round(b, 2)
    expec.append(b)

pred_df = pd.DataFrame({'date': df.index, 
                    'predicted': pred})
expec_df = pd.DataFrame({'date': df.index, 
                    'expected': expec})

from statsmodels.tsa.stattools import acf

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

fa = forecast_accuracy(pred_df.predicted, expec_df.expected)

fa_df= pd.DataFrame(fa,index=[0])


import matplotlib.style as style
style.available
style.use('fivethirtyeight')

fig, ax = plt.subplots(figsize=(16,8))

expec_df.plot(kind='line',x='date',y='expected', color='dodgerblue', ax=ax, label='Gerçek Değer', legend=True)  #expected
pred_df.plot(kind='line',x='date',y='predicted', color='darkorange', ax=ax, label='Tahmin Edilen Değer', legend=True) #predicted

plt.title('ARIMA Yöntemi İle Altın Fiyat Tahmini')
plt.xlabel("Tarih")
plt.ylabel("Altının Fiyatı")

plt.show()
