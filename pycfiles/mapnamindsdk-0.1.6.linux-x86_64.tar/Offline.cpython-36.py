# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mindsdk/Mind/Offline.py
# Compiled at: 2019-12-23 08:11:44
# Size of source mod 2**32: 3384 bytes
import json, urllib
from mindsdk.Mapper import Mapper as mapper
from mindsdk.WS import WS
import mindsdk.Constants as Constants, pandas as pd, cherrypy
from threading import Thread
from mindsdk.Mind.Mind import Mind

class Offline(Mind):

    def getUdsValue(signalNames, startDate, endDate, userId):
        Offline.validate(startDate)
        Offline.validate(endDate)
        try:
            body = {'signalNames':signalNames, 
             'startDate':startDate, 
             'endDate':endDate, 
             'userId':userId}
            targetUrl = 'http://' + Constants.SDK_SERVER_IP + ':' + Constants.SDK_PORT + '/offline/getUsd'
            req = urllib.request.Request(targetUrl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            json_data = json.dumps(body)
            jsonDataAsBytes = json_data.encode('utf-8')
            req.add_header('Content-Length', len(jsonDataAsBytes))
            response = urllib.request.urlopen(req, jsonDataAsBytes)
            jsonResult = response.read()
            listResult = json.loads(jsonResult)
            print(listResult)
            return listResult
        except urllib.error.HTTPError as err:
            print('{}\nError Code:{}, URL:{}'.format(err, err.code, err.filename))
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

    def getValue(signalNames, startDate, endDate, aggregation, interval, pageNumber=1, pageSize=1000):
        try:
            Offline.validate(startDate)
            Offline.validate(endDate)
            f = mapper.Mapper.getInstance()
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
            req = urllib.request.Request(targetUrl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            json_data = json.dumps(body)
            jsonDataAsBytes = json_data.encode('utf-8')
            req.add_header('Content-Length', len(jsonDataAsBytes))
            response = urllib.request.urlopen(req, jsonDataAsBytes)
            jsonResult = response.read()
            df_result = Offline.convertJsonToDataFrame(jsonResult, signalNames)
            return df_result
        except urllib.error.HTTPError as err:
            print('{}\nError Code:{}, URL:{}'.format(err, err.code, err.filename))
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

    def getLastValue(signalNames):
        return super(Offline, Offline).getValue(signalNames)