import pandas as pd                     
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix
from keras.models import Sequential
from keras.layers import Dense, Conv1D, GlobalMaxPooling1D
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import classification_report

df = pd.read_csv("Data Set/Numerical/XAU_1_Year_Over_Sampling.csv", encoding = 'UTF-8', sep=',')
df = df.drop(['Date'], axis=1)

x = df.iloc[:,0:-1]
y = df.iloc[:,-1]

scaler = StandardScaler()
x = scaler.fit_transform(x)

y = to_categorical(y)

x = np.reshape(x, (x.shape[0], x.shape[1], 1))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

model = Sequential()
model.add(Conv1D(128, 2, activation='relu', input_shape=(x_train.shape[1], 1)))
model.add(Conv1D(64, 2, activation='relu'))
model.add(Conv1D(32, 2, activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(2, activation = 'sigmoid'))
model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['acc'])

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
history = model.fit(x_train, y_train, batch_size=4, epochs=100, verbose=1, callbacks=[callback], validation_data = (x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

fig, ax = plt.subplots(2,1, figsize=(12,5))
ax[0].plot(history.history['loss'], label="Training loss")
ax[0].plot(history.history['val_loss'], label="Validation loss",axes =ax[0])
ax[0].set_ylabel("Loss")
ax[0].grid(color='black', linestyle='-', linewidth=0.25)
legend = ax[0].legend(loc='best', shadow=True)

ax[1].plot(history.history['acc'], label="Training accuracy")
ax[1].plot(history.history['val_acc'], label="Validation accuracy")
ax[1].set_xlabel("Number of Epochs")
ax[1].set_ylabel("accuracy")
ax[1].grid(color='black', linestyle='-', linewidth=0.25)
legend = ax[1].legend(loc='best', shadow=True)

y_pred = model.predict(x_test)
y_pred_classes = np.argmax(y_pred,axis = 1) 
y_true = np.argmax(y_test,axis = 1) 
confusion_mtx = confusion_matrix(y_true, y_pred_classes) 
fig, ax = plot_confusion_matrix(conf_mat=confusion_mtx,
                                show_normed=True,
                                figsize =(5,5))

print(classification_report(y_true, y_pred_classes))
