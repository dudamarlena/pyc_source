# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mapnamindsdk/Mind.py
# Compiled at: 2020-01-16 08:29:49
# Size of source mod 2**32: 5995 bytes
import json, datetime, cherrypy, pandas as pd
from threading import Thread
from mapnamindsdk import WS
from mapnamindsdk.Rest import Rest
import mapnamindsdk.Constants as Constants
from mapnamindsdk.Mapper import Mapper as mapper

class Mind(object):

    @staticmethod
    def removeSignal(signalName, userId):
        try:
            body = {'signalName':signalName,  'userId':userId}
            post_req = Rest(f"http://{Constants.SDK_SERVER_IP}:{Constants.SDK_PORT}", path='/remove',
              params=body)
            jsonResult = post_req.post()
            if jsonResult['messageCode'] == '0000':
                return True
            else:
                return False
            return jsonResult
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

    @staticmethod
    def createSignal(signalName, signalDescription, unitMeasurment, userId):
        try:
            body = {'signalName':signalName,  'description':signalDescription, 
             'unitMeasurment':unitMeasurment, 
             'userId':userId}
            post_req = Rest(f"http://{Constants.SDK_SERVER_IP}:{Constants.SDK_PORT}", path='/create',
              params=body)
            jsonResult = post_req.post()
            if jsonResult['messageCode'] == '0000':
                return True
            else:
                return False
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

    @staticmethod
    def setValue(signalName, value, dateAndTime, userId):
        if dateAndTime.lower() != 'now'.lower():
            Mind._validate(dateAndTime)
        body = {'signalName':signalName, 
         'dateAndTime':dateAndTime, 
         'value':value, 
         'userId':userId}
        post_req = Rest(f"http://{Constants.SDK_SERVER_IP}:{Constants.SDK_PORT}", path='/offline/set',
          params=body)
        jsonResult = post_req.post()
        if jsonResult['messageCode'] == '0000':
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
            post_req = Rest(f"http://{Constants.DATASERVICE_SERVER_IP}:{Constants.DATASERVICE_PORT}", path='/online/get',
              params=body)
            listResult = post_req.post()
            dictResult = json.loads(jsonResult)[0]
            return dictResult
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))

    @staticmethod
    def _mapHistorian2DataFrame(x, signalNames):
        """
        Map function for converting each row of the given list (x) to dictionary
        :param x: A single row of list
        :param signalNames: list of signal_names for columns title
        :return: Input list rows in dict format
        """
        try:
            dictCurrentRow = {}
            dictCurrentRow.update({'time': x['time']})
            valueColumns = {signalNames[i]:x['values'][i] for i in range(0, len(signalNames))}
            dictCurrentRow.update(valueColumns)
            return dictCurrentRow
        except:
            print('ERROR:\n')

    @staticmethod
    def _convertJsonToDataFrame(jsonResponse, signalNames):
        """
        Converts given json_response to pandas DataFrame
        :param jsonResponse: Query result in json_response format
        :param signal_names: List of signal names in query to set as columns name of DataFrame
        :return: DataFrame object of json_response
        """
        try:
            mylist = map(lambda x: Mind._mapHistorian2DataFrame(x, signalNames), jsonResponse)
            list_1 = list(mylist)
            dataframe = pd.DataFrame(list_1)
            return dataframe
        except:
            print('ERROR:\n')

    @staticmethod
    def _convertJsonToListOfDict(listResult, signalNames, signalIds):
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

    @staticmethod
    def _validate(date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y/%m/%d-%H:%M:%S')
        except ValueError:
            raise ValueError('Incorrect data format, should be YYYY/MM/DD-HH:mm:SS')