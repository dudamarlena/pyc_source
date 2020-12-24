# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mapnamindsdk/Offline.py
# Compiled at: 2020-01-16 08:41:54
# Size of source mod 2**32: 3345 bytes
import json
from mapnamindsdk.Mapper import Mapper as mapper
import mapnamindsdk.Constants as Constants, pandas as pd
from mapnamindsdk.Rest import Rest
import time
from mapnamindsdk.Mind import Mind

class Offline(Mind):

    @staticmethod
    def getUdsValue(signalNames, startDate, endDate, userId):
        Offline._validate(startDate)
        Offline._validate(endDate)
        try:
            body = {'signalNames':signalNames,  'startDate':startDate, 
             'endDate':endDate, 
             'userId':userId}
            post_req = Rest(f"http://{Constants.SDK_SERVER_IP}:{Constants.SDK_PORT}", path='/offline/getUsd',
              params=body)
            listResult = post_req.post()
            print(listResult)
            return listResult
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

    @staticmethod
    def getValue(signalNames, startDate, endDate, aggregation, interval, pageNumber=1, pageSize=1000):
        jsonResult = None
        t = time.time()
        try:
            Offline._validate(startDate)
            Offline._validate(endDate)
            f = mapper.getInstance()
            signalIDs = list(map(lambda x: int(f.SignalMapper[x]), signalNames))
            units = list(map(lambda x: int(x[0:2]), signalNames))
            body = {'ids':signalIDs, 
             'units':units, 
             'from_date':startDate, 
             'to_date':endDate, 
             'agg':aggregation, 
             'interval':interval, 
             'page_size':pageSize, 
             'page_number':pageNumber}
            targetUrl = 'http://' + Constants.SDK_SERVER_IP + ':' + Constants.SDK_PORT + '/offline/get'
            post_req = Rest(f"http://{Constants.SDK_SERVER_IP}:{Constants.SDK_PORT}", path='/offline/get',
              params=body)
            jsonResult = post_req.post()
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

        df_result = Offline._convertJsonToDataFrame(jsonResult, signalNames)
        return df_result

    @staticmethod
    def getValue2(signalNames, timeRanges: list, aggregation, interval, pageNumber=1, pageSize=1000) -> pd.DataFrame:
        final_result = pd.DataFrame([])
        for range in timeRanges:
            startDate = range[0]
            endDate = range[1]
            df = Offline.getValue(signalNames, startDate=startDate, endDate=endDate, aggregation=aggregation, interval=interval,
              pageNumber=pageNumber,
              pageSize=pageSize)
            final_result = pd.concat([final_result, df])

        return final_result

    @staticmethod
    def getLastValue(signalNames):
        return super(Offline, Offline).getValue(signalNames)