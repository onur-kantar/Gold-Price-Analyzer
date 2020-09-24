import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

data = pd.read_csv(r"C:\Users\onur\Desktop\Staj\Veri Kümeleri\Sayısal\XAU_1_Year_Over_Sampling.csv", encoding = 'UTF-8', sep=',')
data = data.drop(['Date'], axis=1)

x = data.iloc[:,1:5]
y = data.iloc[:,1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

regr = LinearRegression()
regr.fit(x_train,y_train)
y_pred = regr.predict(x_test)
print("Linear Regression")
print("R score: {0}".format(round(regr.score(x_train, y_train))))
print("Intercept: {0}".format(round(regr.intercept_)))
mae = mean_absolute_error(regr.predict(x_test), y_test)
mse = mean_squared_error(regr.predict(x_test), y_test)
mape = mean_absolute_percentage_error(regr.predict(x_test), y_test)
rmse = np.sqrt(mse)
print('Mean Absolute Error (MAE): %.2f' % mae)
print('Mean Squared Error (MSE): %.2f' % mse)
print('Root Mean Squared Error (RMSE): %.2f' % rmse)
print(pd.DataFrame({'feature':x.columns, 'coef':regr.coef_}))

regr = DecisionTreeRegressor()
regr.fit(x_train,y_train)
y_pred = regr.predict(x_test)
print("Decision Tree Regression")
print("R score: {0}".format(round(regr.score(x_train, y_train))))
mae = mean_absolute_error(regr.predict(x_test), y_test)
mse = mean_squared_error(regr.predict(x_test), y_test)
mape = mean_absolute_percentage_error(regr.predict(x_test), y_test)
rmse = np.sqrt(mse)
print('Mean Absolute Error (MAE): %.2f' % mae)
print('Mean Squared Error (MSE): %.2f' % mse)
print('Root Mean Squared Error (RMSE): %.2f' % rmse)

regr = RandomForestRegressor(n_estimators=300, random_state = 42)
regr.fit(x_train,y_train)
y_pred = regr.predict(x_test)
print("Random Forest Regression")
print("R score: {0}".format(round(regr.score(x_train, y_train))))
mae = mean_absolute_error(regr.predict(x_test), y_test)
mse = mean_squared_error(regr.predict(x_test), y_test)
mape = mean_absolute_percentage_error(regr.predict(x_test), y_test)
rmse = np.sqrt(mse)
print('Mean Absolute Error (MAE): %.2f' % mae)
print('Mean Squared Error (MSE): %.2f' % mse)
print('Root Mean Squared Error (RMSE): %.2f' % rmse)


polynomial_reg = PolynomialFeatures(degree=4)
model = LinearRegression()
model = model.fit(x_train, y_train)
y_pred = model.predict(x_test)
y_pred = np.round_(y_pred)
print("Polynomial Regression")
print("R score: {0}".format(round(regr.score(x_train, y_train))))
mae = mean_absolute_error(regr.predict(x_test), y_test)
mse = mean_squared_error(regr.predict(x_test), y_test)
mape = mean_absolute_percentage_error(regr.predict(x_test), y_test)
rmse = np.sqrt(mse)
print('Mean Absolute Error (MAE): %.2f' % mae)
print('Mean Squared Error (MSE): %.2f' % mse)
print('Root Mean Squared Error (RMSE): %.2f' % rmse)
