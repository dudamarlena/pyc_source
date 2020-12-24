# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mindsdk/Mind/Mind.py
# Compiled at: 2019-12-24 02:25:02
# Size of source mod 2**32: 7780 bytes
import json, urllib, datetime, pandas as pd
from mindsdk.Mapper import Mapper as mapper
from mindsdk.WS import WS
import mindsdk.Constants as Constants, cherrypy
from threading import Thread

class Mind(object):

    def __init__(self):
        pass

    def removeSignal(signalName, userId):
        try:
            body = {'signalName':signalName, 
             'userId':userId}
            targetUrl = 'http://' + Constants.SDK_SERVER_IP + ':' + Constants.SDK_PORT + '/remove'
            req = urllib.request.Request(targetUrl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            json_data = json.dumps(body)
            jsonDataAsBytes = json_data.encode('utf-8')
            req.add_header('Content-Length', len(jsonDataAsBytes))
            response = urllib.request.urlopen(req, jsonDataAsBytes)
            jsonResult = response.read()
            listResult = json.loads(jsonResult)
            if listResult['messageCode'] == '0000':
                return True
            else:
                return False
            return jsonResult
        except urllib.error.HTTPError as err:
            print('{}\nError Code:{}, URL:{}'.format(err, err.code, err.filename))
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

    def createSignal(signalName, signalDescription, unitMeasurment, userId):
        try:
            body = {'signalName':signalName, 
             'description':signalDescription, 
             'unitMeasurment':unitMeasurment, 
             'userId':userId}
            targetUrl = 'http://' + Constants.SDK_SERVER_IP + ':' + Constants.SDK_PORT + '/create'
            req = urllib.request.Request(targetUrl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            json_data = json.dumps(body)
            jsonDataAsBytes = json_data.encode('utf-8')
            req.add_header('Content-Length', len(jsonDataAsBytes))
            response = urllib.request.urlopen(req, jsonDataAsBytes)
            jsonResult = response.read()
            listResult = json.loads(jsonResult)
            if listResult['messageCode'] == '0000':
                return True
            else:
                return False
        except urllib.error.HTTPError as err:
            print('{}\nError Code:{}, URL:{}'.format(err, err.code, err.filename))
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

    def setValue(signalName, value, dateAndTime, userId):
        if dateAndTime.lower() != 'now'.lower():
            Mind.validate(dateAndTime)
        body = {'signalName':signalName, 
         'dateAndTime':dateAndTime, 
         'value':value, 
         'userId':userId}
        targetUrl = 'http://' + Constants.SDK_SERVER_IP + ':' + Constants.SDK_PORT + '/offline/set'
        req = urllib.request.Request(targetUrl)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        json_data = json.dumps(body)
        jsonDataAsBytes = json_data.encode('utf-8')
        req.add_header('Content-Length', len(jsonDataAsBytes))
        response = urllib.request.urlopen(req, jsonDataAsBytes)
        jsonResult = response.read()
        listResult = json.loads(jsonResult)
        if listResult['messageCode'] == '0000':
            return True
        else:
            return False
            return jsonResult

    @staticmethod
    def getValue(signalNames):
        """
        Get value from ONLINE table
        :return:
        """
        try:
            f = mapper.Mapper.getInstance()
            signalID = int(f.SignalMapper[signalNames])
            body = {'ids':[
              signalID], 
             'type':'TIMESERIES'}
            targetUrl = 'http://' + Constants.DATASERVICE_SERVER_IP + ':' + Constants.DATASERVICE_PORT + '/online/get'
            req = urllib.request.Request(targetUrl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            jsonData = json.dumps(body)
            jsonDataAsBytes = jsonData.encode('utf-8')
            req.add_header('Content-Length', len(jsonDataAsBytes))
            response = urllib.request.urlopen(req, jsonDataAsBytes)
            jsonResult = response.read()
            dictResult = json.loads(jsonResult)[0]
            return dictResult
        except urllib.error.HTTPError as err:
            print('{}\nError Code:{}, URL:{}'.format(err, err.code, err.filename))
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

    @staticmethod
    def mapHistorian2DataFrame(x, signalNames):
        """
        Map function for converting each row of the given list (x) to dictionary
        :param x: A single row of list
        :param signalNames: list of signal_names for columns title
        :return: Input list rows in dict format
        """
        dictCurrentRow = {}
        dictCurrentRow.update({'time': x['time']})
        valueColumns = {signalNames[i]:x['values'][i] for i in range(0, len(signalNames))}
        dictCurrentRow.update(valueColumns)
        return dictCurrentRow

    @staticmethod
    def convertJsonToDataFrame(jsonResponse, signalNames):
        """
        Converts given json_response to pandas DataFrame
        :param jsonResponse: Query result in json_response format
        :param signal_names: List of signal names in query to set as columns name of DataFrame
        :return: DataFrame object of json_response
        """
        listResult = json.loads(jsonResponse)
        mylist = map(lambda x: Mind.mapHistorian2DataFrame(x, signalNames), listResult)
        list_1 = list(mylist)
        dataframe = pd.DataFrame(list_1)
        return dataframe

    def convertJsonToListOfDict(listResult, signalNames, signalIds):
        ii = 0
        totaldict = {}
        for i in listResult:
            dict = i
            mediumlist = dict.get(str(signalIds[ii]))
            listofvaluetimetotal = []
            for l in mediumlist:
                time = l.get('TIME')
                value = l.get('VALUE')
                listofvaluetime = [time, value]
                listofvaluetimetotal.append(listofvaluetime)

            totaldict[signalNames[ii]] = listofvaluetimetotal
            ii = ii + 1

        print(totaldict)
        return totaldict

    def validate(date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y/%m/%d-%H:%M:%S')
        except ValueError:
            raise ValueError('Incorrect data format, should be YYYY/MM/DD-HH:mm:SS')