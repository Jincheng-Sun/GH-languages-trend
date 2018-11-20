import jsonlines
import datetime
import numpy as np
from sklearn.preprocessing import MinMaxScaler
filename='iterm.jl'

def parseJson(lang):
    dataset=[]
    with open(filename, 'r+', encoding='utf8') as f:
        for item in jsonlines.Reader(f):
            l=''
            n=0
            for i in range(0,10):

                if(item['n%dlang'%(i+1)]==lang):
                    n=float(item['n%dnum'%(i+1)])

            # timestamp = datetime.datetime.strptime(item['timestamp'], "%Y-%m-%dT%H:%M:%S")
            #
            # startday = datetime.datetime(2009,1,1,0,0)
            #
            # days=int((timestamp-startday).days)

            if(n!=0):
                dataset.append([n])

    dataset=np.array(dataset)
    trainSeq = dataset[0:int(len(dataset) * 0.8)]
    testSeq = dataset[int(len(dataset) * 0.8):len(dataset)]

    return trainSeq,testSeq,dataset

def fillBlank(array):
    for i in range(array.shape[0]):
        if(array[i][0]== 0 and i>=15):
            array[i][0]=np.sum(array[(i-15):(i+15)])/31
            print(array[i][0])

    return array

# scaler = MinMaxScaler(feature_range=(0, 1))
# dataset = scaler.fit_transform(dataset)


def create_dataset(dataseq,look_back=7):
    dataX, dataY = [], []
    for i in range(len(dataseq) - look_back - 1):
        a = dataseq[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataseq[i + look_back, 0])
    return np.array(dataX), np.array(dataY)





