''' model training '''
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils

from sklearn.model_selection import train_test_split


root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

from tictactoe.game import Game


def plot_accuracy_graphs(history, epochs):
    """This function plots the loss curves, allowing overfitting (if present) to be detected.

    Args:
        history (dataframe): the model and its parameters
        epochs (integer): the number of x-axis intervals chosen to plot the loss curves
        display (bool, optional): Set to True if you want loss curves to be printed to screen. Defaults to False.

    Returns:
        Graph of the loss curves
    """
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    plt.ylim([0, 1.0])

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.ylim([0, 1.0])

    return plt.show()

training_iteration = 5

train_valid_split_ratio = 0.2
data = pd.read_pickle(root + r'/data/data_{0}.pkl'.format(str(training_iteration)))

outputmap = {'X': 0, 'O': 1, 'D':2}
data['winner'] = data['winner'].map(outputmap)
data = data[data['winner'].isin([0, 1])]

x = np.array(list(data['board'].copy()))
y = np.array(data['winner'].copy())

x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=train_valid_split_ratio, random_state=0)

# Get number of classes
nr_classes = len(np.unique(y_train))

# Convert y classes to categorical features for keras model
y_train = np_utils.to_categorical(y_train, nr_classes)
y_valid = np_utils.to_categorical(y_valid, nr_classes)

# Construct model
model = Sequential()

model.add(Dense(9, input_shape=x_train.shape[1:], activation="relu"))
model.add(Dense(18, activation="relu"))
model.add(Dense(9, activation="relu"))
model.add(Dense(4, activation="relu"))
model.add(Dense(nr_classes, activation="sigmoid"))

# compile the model
model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=['accuracy'])

model.summary()

batch = 50
epochs = 40
# Fit the model
history = model.fit(
    x_train, y_train,
    batch_size=batch,
    epochs=epochs,
    verbose=2,
    validation_data=(x_valid, y_valid),
    )

plot_accuracy_graphs(history, epochs)

model.save('model_%s.h5' %(str(training_iteration)))
