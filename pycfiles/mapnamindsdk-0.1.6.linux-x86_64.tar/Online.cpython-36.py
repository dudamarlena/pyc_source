# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mindsdk/Mind/Online.py
# Compiled at: 2019-12-23 00:16:47
# Size of source mod 2**32: 2884 bytes
import json, urllib
from mindsdk.Mapper import Mapper as mapper
from mindsdk.WS import WS
import mindsdk.Constants as Constants, cherrypy
from threading import Thread
from mindsdk.Mind.Mind import Mind

class Online(Mind):

    def __init__(self):
        super(Online, self).__init__()

    @staticmethod
    def _startWS():
        cherrypy.quickstart(WS.MindSdkWebService)

    @staticmethod
    def startWS():
        Thread(target=(Online._startWS)).start()

    @staticmethod
    def callback():
        print('finished!')

    @staticmethod
    def set(key, value):
        WS.MindSdkWebService.set(key=key, value=value)

    @staticmethod
    def add(key, value):
        WS.MindSdkWebService.add(key=key, value=value)

    @staticmethod
    def getResult(key):
        return WS.MindSdkWebService.getResult(key)

    @staticmethod
    def getResultList(key):
        return WS.MindSdkWebService.getList(key)

    @staticmethod
    def getValue(signalNames, startDate, endDate, userId):
        Mind.validate(startDate)
        Mind.validate(endDate)
        try:
            body = {'signalNames':signalNames, 
             'startTime':startDate, 
             'endTime':endDate, 
             'userId':userId}
            targetUrl = 'http://' + Constants.SDK_SERVER_IP + ':' + Constants.SDK_PORT + '/online/get'
            req = urllib.request.Request(targetUrl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            json_data = json.dumps(body)
            jsonDataAsBytes = json_data.encode('utf-8')
            req.add_header('Content-Length', len(jsonDataAsBytes))
            response = urllib.request.urlopen(req, jsonDataAsBytes)
            jsonResult = response.read()
            listResult = json.loads(jsonResult)
            return listResult
        except urllib.error.HTTPError as err:
            print('{}\nError Code:{}, URL:{}'.format(err, err.code, err.filename))
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))