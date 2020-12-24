# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mapnamindsdk/Online.py
# Compiled at: 2020-01-16 08:26:51
# Size of source mod 2**32: 1930 bytes
import json, cherrypy
from threading import Thread
from mapnamindsdk import WS
from mapnamindsdk.Rest import Rest
from mapnamindsdk.Mind import Mind
from mapnamindsdk import Mapper as mapper
import mapnamindsdk.Constants as Constants

class Online(Mind):

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
        Mind._validate(startDate)
        Mind._validate(endDate)
        try:
            body = {'signalNames':signalNames,  'startTime':startDate, 
             'endTime':endDate, 
             'userId':userId}
            request = Rest(f"http://{Constants.SDK_SERVER_IP}:{Constants.SDK_PORT}", path='/online/get', params=body)
            jsonResult = request.post(get_json=True)
            return jsonResult
        except KeyError as err:
            print('ERROR: Signal Name {} not found!\n'.format(err))


if __name__ == '__main__':
    params = {'par1':'value1', 
     'par2':3}
    req = Rest(base_url='https://postman-echo.com', path='/get',
      params=params)
    post_req = Rest(base_url='https://postman-echo.com', path='/post',
      params=params)
    print(req.get())