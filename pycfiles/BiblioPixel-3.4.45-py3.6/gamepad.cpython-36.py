# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/gamepad.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 271 bytes


class BaseGamePad(object):

    def __init__(self):
        pass

    def getKeys(self):
        raise Exception('getKeys must be overriden!')

    def close(self):
        pass

    def setLights(self, data):
        pass

    def setLightsOff(self, count):
        pass