import os
import numpy as np
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

import matplotlib.pyplot as plt


def load_data():
    DATABASE_PATH = os.path.join(os.getcwd(), 'dataset', 'data.pkl')
    
    X, Y = [], []

    with open(DATABASE_PATH, 'rb') as fl:
        data = pickle.load(fl)

    for frame in data:
        X.append(np.array(frame[0]))
        Y.append(frame[1])

    X, Y = np.array(X), np.array(Y)
    return X, Y

def prepare_data(test_size=0.2):
    X, y = load_data()
    le = LabelEncoder()
    classess = list(set(y))
    y = le.fit_transform(y)
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=test_size)
    return X_train, X_valid, y_train, y_valid, classess

def build_model(input_shape, classes):

    model = Sequential()
    model.add(LSTM(128, input_shape=input_shape, activation='relu', return_sequences=True))
    model.add(LSTM(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(classes, activation='softmax'))

    opt = Adam(learning_rate=1e-4, decay=1e-6)
    model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    print(model.summary())

    return model

def plot_history(history):
    fig, axs = plt.subplots(2)
    axs[0].plot(history.history['accuracy'], label="Train Accuracy")
    axs[0].plot(history.history['val_accuracy'], label="Test Accuracy")
    axs[0].set_ylabel("Accuracy")
    axs[0].set_xlabel("Epoch")
    axs[0].set_title("Accuracy Eval")

    axs[1].plot(history.history['loss'], label="Train Loss")
    axs[1].plot(history.history['val_loss'], label="Test Loss")
    axs[1].set_ylabel("Loss")
    axs[1].set_xlabel("Epoch")
    axs[1].set_title("Loss Eval")

    fig.tight_layout()

    plt.savefig('acc_loss.png')
    plt.show()



if __name__ == '__main__':
    X_train, X_valid, y_train, y_valid, classess = prepare_data()

    model = build_model(X_train.shape[1:], len(classess))
    my_callbacks = [tf.keras.callbacks.EarlyStopping(patience=2)]

    history = model.fit(X_train, y_train, validation_data = (X_valid, y_valid), batch_size = 32, epochs = 100, callbacks=my_callbacks)
    model.save('dataset/gait_model.h5')

    plot_history(history)
