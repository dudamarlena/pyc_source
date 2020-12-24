# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mindsdk/Mapper/Mapper.py
# Compiled at: 2019-12-19 05:39:37
# Size of source mod 2**32: 1425 bytes
import urllib.request, urllib.parse, json, mindsdk.Constants as Constants

class Mapper:
    _Mapper__instance = None
    SignalMapper = None

    @staticmethod
    def getInstance():
        if Mapper._Mapper__instance == None:
            Mapper()
        return Mapper._Mapper__instance

    @staticmethod
    def getMapper():
        try:
            url = 'http://' + Constants.SIGNALSERVICE_SERVER_IP + ':' + Constants.SIGNALSERVICE_PORT + '/getmapper'
            f = urllib.request.urlopen(url)
            jsonResponse = f.read().decode('utf-8')
            dictResponse = json.loads(jsonResponse)
            dictResult = {}
            for signal in dictResponse:
                if dictResponse[signal]['plantId'] == 3:
                    dictResult[dictResponse[signal]['signalName']] = signal

            return dictResult
        except urllib.error.HTTPError as err:
            print('{}\nError Code:{}, URL:{}'.format(err, err.code, err.filename))
            return

    def __init__(self):
        """ Virtually private constructor. """
        if Mapper._Mapper__instance != None:
            raise Exception('This class is a singleton!')
        else:
            Mapper.SignalMapper = Mapper.getMapper()
            Mapper._Mapper__instance = self