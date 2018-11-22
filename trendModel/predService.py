import numpy as np
import datetime
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from createDataset import parseJson, create_dataset
import os

path = os.path.dirname(os.path.realpath(__file__))


def train_model(lang):
    look_back = 7
    language = lang
    trainSeq, testSeq, dataset = parseJson(language)
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataSequence = scaler.fit_transform(dataset)
    inputX, inputY = create_dataset(dataSequence, look_back=look_back)

    inputX = np.reshape(inputX, (inputX.shape[0], 1, inputX.shape[1]))
    # inverse=scaler.inverse_transform(dataSequence)

    model = Sequential()
    model.add(LSTM(10, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(inputX, inputY, epochs=int(float(dataset.shape[0]) / 10), batch_size=100, verbose=10)
    model.save(path + '/models/%smodel.h5' % language)


def pred(timestamp, lang):
    # time_value[timestamp,repo_number]
    time_value = pd.read_csv('datas/%sdata.csv' % lang, encoding='gb18030')
    # bottom of time_value
    time_last = time_value.loc[time_value.shape[0] - 1]['timestamp']
    # input of model
    datas = np.array(time_value.loc[time_value.shape[0] - 7:time_value.shape[0] - 1]['repo_number'])
    datas = np.reshape(datas, [7, 1])
    # normalize input

    scaler = MinMaxScaler(feature_range=(0, 1))
    datas = scaler.fit_transform(datas)
    dataSequence = np.reshape(datas, (1, 1, 7))
    # load model
    model = load_model(path + '/models/%smodel.h5' % lang)
    # predict
    pre = scaler.inverse_transform(model.predict(dataSequence))
    # write in csv
    time_last = datetime.datetime.strptime(time_last, "%Y-%m-%d %H:%M:%S")
    time_new = time_last + datetime.timedelta(days=1)
    time_value.append([time_new, pre])
    time_value.to_csv(path + 'datas/%sdata.csv' % lang, encoding='gb18030')

    # 清理内存
    del time_value
    del model

    if ((timestamp - time_last).days == 1):
        tempSeq = None

        return 1
    else:
        return predTill(timestamp + datetime.timedelta(days=-1), lang)


def predTill(timestamp, lang):
    # load model
    try:
        model = load_model(path + '/models/%smodel.h5' % lang)
    except:
        print('[LOG]:no model found, start training...')
        train_model(lang)
        model = load_model(path + '/models/%smodel.h5' % lang)
    # load data
    time_value = pd.read_csv(path + '/datas/%sdata.csv' % lang, encoding='gb18030')
    time_value = pd.DataFrame(time_value, columns=['timestamp', 'repo_number'])
    time_value = np.array(time_value)
    # output
    pred = []

    time_last = time_value[time_value.shape[0] - 1][0]
    time_last = datetime.datetime.strptime(time_last, "%Y-%m-%d %H:%M:%S")

    while ((timestamp - time_last).days != 0):
        # get last 7 days' data
        datas = np.array(time_value[time_value.shape[0] - 7:time_value.shape[0], 1])
        datas = np.reshape(datas, [7, 1])
        scaler = MinMaxScaler(feature_range=(0, 1))
        datas = scaler.fit_transform(datas)
        dataSequence = np.reshape(datas, (1, 1, 7))
        pre = scaler.inverse_transform(model.predict(dataSequence))
        print(pre[0][0])

        time_last = time_last + datetime.timedelta(days=1)
        print(time_value.shape)
        update = np.reshape(['pre', pre[0][0]], [1, 2])
        time_value = np.append(time_value, update, axis=0)
        print(time_value.shape)
        # output
        # pred.append(pre)
        pred = np.append(pred, int(pre))

    return pred

# a=predTill(datetime.datetime(2018,11,18),'Python')
train_model('JavaScript')