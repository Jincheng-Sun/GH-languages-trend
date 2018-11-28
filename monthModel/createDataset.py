import jsonlines
import datetime
import numpy as np
import pandas as pd
from pymongo import MongoClient
import os
path=os.path.dirname(os.path.realpath(__file__))

connection = MongoClient('0.0.0.0',27017)

db = connection.GHUserAnalyse

set = db.MonAvgLang

def parseJson(lang,total=False):
    dataset=[]
    results = set.find({'language': lang})
    for result in results:
        dataset.append([result['month_avg']])

    dataset=np.array(dataset)
    trainSeq = dataset[0:int(len(dataset) * 0.8)]
    testSeq = dataset[int(len(dataset) * 0.8):len(dataset)]
    connection.close()
    return trainSeq,testSeq,dataset

def create_dataset(dataseq,look_back=12):
    dataX, dataY = [], []
    for i in range(len(dataseq) - look_back - 1):
        a = dataseq[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataseq[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


