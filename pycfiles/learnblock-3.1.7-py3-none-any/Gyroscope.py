# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/Clients/Devices/Gyroscope.py
# Compiled at: 2019-04-07 11:14:14


class Gyroscope:
    """
    Gyroscope is a class that contain the values rx, ry, rz of a Gyroscope in rad.
    """
    rx = None
    ry = None
    rz = None

    def __init__(self, _readFunction):
        self.__readDevice = _readFunction

    def set(self, _rx, _ry, _rz):
        self.rx, self.ry, self.rz = _rx, _ry, _rz

    def get(self):
        return (
         self.rx, self.ry, self.rz)

    def read(self):
        _rx, _ry, _rz = self.__readDevice()
        self.set(_rx, _ry, _rz)