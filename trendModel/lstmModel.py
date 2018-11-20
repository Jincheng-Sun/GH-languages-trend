import h5py
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from createDataset import parseJson, create_dataset

import matplotlib.pyplot as plt

look_back = 7
language = 'Python'
trainSeq, testSeq, dataset = parseJson(language)


def train_model(trainseq):
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataSequence = scaler.fit_transform(trainseq)
    inputX, inputY = create_dataset(dataSequence, look_back=look_back)

    inputX = np.reshape(inputX, (inputX.shape[0], 1, inputX.shape[1]))
    # inverse=scaler.inverse_transform(dataSequence)

    model = Sequential()
    model.add(LSTM(10, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(inputX, inputY, epochs=int(float(trainseq.shape[0]) / 10), batch_size=100, verbose=10)
    model.save('%smodel.h5' % language)


def predict(testseq):
    scaler = MinMaxScaler(feature_range=(0, 1))
    model = load_model('%smodel.h5' % language)
    dataSequence = scaler.fit_transform(testseq)
    testX, testY = create_dataset(dataSequence, look_back=look_back)
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    Pre = scaler.inverse_transform(model.predict(testX))
    Real = scaler.inverse_transform(np.reshape(testY, [len(testY), 1]))
    return Pre, Real





def plot(dataset, trainPredict):
    trainPredictPlot = np.empty_like(dataset)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict
    plt.subplot(dataset, label='Actual')
    plt.subplot()
    plt.show()
    return trainPredictPlot


def plotall():
    p, r = predict(testSeq)
    p2, r2 = predict(trainSeq)
    trainPredictPlot = np.empty_like(dataset)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(p2) + look_back, :] = p2

    testPredictPlot = np.empty_like(dataset)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(p2) + (look_back * 2) + 1:len(dataset) - 1, :] = p
    plt.plot(dataset, label='Actual')
    plt.plot(trainPredictPlot, label='trainset')
    plt.plot(testPredictPlot, label='test')
    plt.show()
