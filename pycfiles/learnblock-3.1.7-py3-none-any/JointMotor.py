# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pilar/robocomp/components/learnbot/learnbot_dsl/Clients/Devices/JointMotor.py
# Compiled at: 2019-04-07 11:14:14


class JointMotor:

    def __init__(self, _callDevice, _readDevice):
        self._callDevice = _callDevice
        self._readDevice = _readDevice
        self._angle = 0

    def sendAngle(self, _angle):
        self._callDevice(_angle)
        self._angle = _angle

    def getAngle(self):
        return self._angle

    def read(self):
        _angle = self._readDevice()