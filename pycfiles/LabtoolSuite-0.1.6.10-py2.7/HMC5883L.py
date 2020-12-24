# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Labtools/HMC5883L.py
# Compiled at: 2015-05-09 06:16:36
import Labtools.interface as interface, time
from numpy import int16

class HMC5883L:

    def __init__(self, ADDRESS=30):
        self.ADDRESS = ADDRESS
        self.I = interface.Interface()

    def connect(self):
        self.I.I2C.start(self.ADDRESS, 0)
        self.I.I2C.send(1)
        self.I.I2C.send(0)
        self.I.I2C.stop()
        self.I.I2C.start(self.ADDRESS, 0)
        self.I.I2C.send(2)
        self.I.I2C.send(0)
        self.I.I2C.stop()

    def __getVals__(self, addr, bytes):
        self.I.I2C.start(self.ADDRESS, 0)
        self.I.I2C.send(addr)
        self.I.I2C.restart(self.ADDRESS, 1)
        vals = self.I.I2C.read(bytes)
        self.I.I2C.stop()
        return vals

    def read(self):
        vals = self.__getVals__(3, 6)
        x = int16(vals[0] << 8 | vals[1])
        y = int16(vals[2] << 8 | vals[3])
        z = int16(vals[4] << 8 | vals[5])
        return (x, y, z)