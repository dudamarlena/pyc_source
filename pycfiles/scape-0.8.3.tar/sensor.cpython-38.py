# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\develop\code\Python\scape\scape\template\project_name\sensors\sensor.py
# Compiled at: 2020-04-20 09:37:54
# Size of source mod 2**32: 266 bytes
from scape.signal.sensor import SignalSensor

class SensorDemo(SignalSensor):

    def __init__(self):
        super().__init__()

    @staticmethod
    def signal_0():
        return 'say'

    @staticmethod
    def signal_1():
        return 'hello'