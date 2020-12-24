# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mapnamindsdk/Mapper.py
# Compiled at: 2020-01-16 08:27:32
# Size of source mod 2**32: 1110 bytes
import json
from mapnamindsdk.Rest import Rest
from mapnamindsdk import Constants

class Mapper:
    _Mapper__instance = None
    SignalMapper = None

    def __init__(self):
        """ Virtually private constructor. """
        if Mapper._Mapper__instance != None:
            raise Exception('This class is a singleton!')
        else:
            Mapper.SignalMapper = Mapper.getMapper()
            Mapper._Mapper__instance = self

    @staticmethod
    def getInstance():
        if Mapper._Mapper__instance == None:
            Mapper()
        return Mapper._Mapper__instance

    @staticmethod
    def getMapper():
        try:
            request = Rest(f"http://{Constants.SIGNALSERVICE_SERVER_IP}:{Constants.SIGNALSERVICE_PORT}",
              path='/getmapper')
            dictResponse = request.get(get_json=True)
            dictResult = {}
            for signal in dictResponse:
                if dictResponse[signal]['plantId'] == 3:
                    dictResult[dictResponse[signal]['signalName']] = signal

        except Exception as e:
            print(str(e))
            return

        return dictResult