# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/Clients/Devices/Acelerometer.py
# Compiled at: 2019-04-07 11:14:14


class Acelerometer:
    """
    Acelerometer is a class that contain the values rx, ry, rz of a Acelerometer in rad.
    """
    _x = None
    _y = None
    _z = None

    def __init__(self, _readFunction):
        self._readDevice = _readFunction

    def set(self, _x, _y, _z):
        self._x, self._y, self._z = _x, _y, _z

    def get(self):
        return (
         self._x, self._y, self._z)

    def read(self):
        _x, _y, _z = self._readDevice()
        self.set(_x, _y, _z)