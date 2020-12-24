# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/Clients/Devices/DistanceSensors.py
# Compiled at: 2019-04-07 11:14:14


class DistanceSensors:
    __distanceSensor = {'front': [0], 'left': [
              0], 
       'right': [
               0], 
       'back': [
              0], 
       'bottom': [
                0]}

    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def set(self, key, values):
        self.__distanceSensor[key] = values

    def read(self):
        dictValues = self._readDevice()
        for key in dictValues:
            self.set(key, dictValues[key])

    def get(self):
        return self.__distanceSensor