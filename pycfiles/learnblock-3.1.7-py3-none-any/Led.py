# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/Clients/Devices/Led.py
# Compiled at: 2019-04-07 11:14:14
from enum import Enum

class LedStatus(Enum):
    ON = True
    OFF = False


class Led:

    def __init__(self, _setState=None, _readState=None):
        self._State = None
        self._setState = _setState
        self._readState = _readState
        return

    def setState(self, _status):
        self._setState(_status)
        _State = _status

    def read(self):
        if self._readState is not None:
            self._State = self._readState()
        return

    def getState(self):
        return self._State


class RGBLed:

    def __init__(self, _setColorState=None, _readState=None):
        self._State = None
        self._readState = _readState
        self._setColorState = _setColorState
        return

    def setColorState(self, _r, _g, _b):
        if self._setColorState is not None:
            self._setColorState(_r, _g, _b)
            self._State = (_r, _g, _b)
        return

    def read(self):
        if self._readState is not None:
            self._State = self._readState()
        return

    def getState(self):
        return self._State