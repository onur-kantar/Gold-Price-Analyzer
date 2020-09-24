import pandas as pd                     
from sklearn.preprocessing import StandardScaler
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from sklearn.metrics import confusion_matrix
from mlxtend.plotting import plot_confusion_matrix
from keras.models import Sequential
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.layers import Dense, SimpleRNN

df = pd.read_csv("Data Set/Twitter/Twitter_Augmented.csv", encoding = 'UTF-8', sep=',')

x = df['tweet']
y = df['target']

token = Tokenizer()
token.fit_on_texts(x)
x = token.texts_to_sequences(x)
x = pad_sequences(x)

scaler = StandardScaler()
x = scaler.fit_transform(x)

y = to_categorical(y)

x = np.reshape(x, (x.shape[0], x.shape[1], 1))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

model = Sequential()
model.add(SimpleRNN(units = 16, activation = "relu", return_sequences = True, input_shape = (x_train.shape[1], 1)))
model.add(SimpleRNN(units = 8, activation = "relu", return_sequences = True))
model.add(SimpleRNN(units = 4, activation = "relu"))
model.add(Dense(2, activation = "sigmoid"))
model.compile(loss='binary_crossentropy',
                optimizer='adam', 
                metrics=['acc'])

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
history = model.fit(x_train, y_train, batch_size = 32, epochs = 100, callbacks=[callback], verbose = 1, validation_data = (x_test, y_test))

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
