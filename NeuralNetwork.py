#import keras
#import theano

import numpy as np
import scipy
import pandas as pd
from itertools import islice

from keras.engine import Model
from keras.layers import Input, TimeDistributed, Flatten
from keras.models import Sequential
from keras.layers import LSTM
from keras.activations import relu
from keras.layers import Activation
from keras.layers import Reshape
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import TimeDistributedDense
import numpy as np

'''Neural Network class.

This class sets up the neural network, taking the input data, respective labels,
the batch size and the number of epochs to run as arguments. The data and labels should be numpy arrays of equal length, with data and corresponding label at the same index of their respective arrays.'''



class NeuralNetwork:
    def __init__(self,batch_size,epochs, data, labels):
        self.batch_size = batch_size
        self.epochs = epochs
        self.data = data
        self.labels = labels

    def setupNetwork(self, x_shape,y_shape, dims, dimslabels, seqlength):
        x = np.array(self.data)
        x = x.reshape(x_shape)
        y = np.array(self.labels)
        y = y.reshape(y_shape)
        model = Sequential()
        model.add(
            TimeDistributed(Dense(output_dim=dims, input_dim=dims),input_shape=(seqlength,dims))) # Add a time-distributed (inputs are sequential and output at time t is fed as input at time t-1
        model.add(LSTM(50, dropout_W=0, dropout_U=0, activation='relu')) #add Long Short-Term Memory Layer
        #model.add(Dense(25, activation='relu'))
        print(model.get_input_shape_at(0))
        print(model.get_output_shape_at(0))
        model.add(Dense(dimslabels,activation='relu'))
        model.compile(loss='categorical_crossentropy',
                      optimizer='rmsprop',
                     metrics=['accuracy','mean_squared_error'])
        model.fit(x,y, batch_size=self.batch_size, nb_epoch=self.epochs, verbose=2,validation_split=0.1)