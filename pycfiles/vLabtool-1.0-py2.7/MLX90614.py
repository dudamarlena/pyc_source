# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/SENSORS/MLX90614.py
# Compiled at: 2015-07-23 04:44:51
from numpy import int16

class MLX90614:
    NUMPLOTS = 1

    def __init__(self, I2C, **args):
        self.I2C = I2C
        self.ADDRESS = args.get('address', 90)
        self.OBJADDR = 7
        self.AMBADDR = 6
        self.source = self.OBJADDR
        self.name = 'Passive IR temperature sensor'
        self.params = {'readReg': range(32), 'select_source': [
                           'object temperature', 'ambient temperature']}
        try:
            print 'switching baud to 100k'
            self.I2C.configI2C(100000.0)
        except:
            print 'FAILED TO CHANGE BAUD RATE'

    def select_source(self, source):
        if source == 'object temperature':
            self.source = self.OBJADDR
        elif source == 'ambient temperature':
            self.source = self.AMBADDR

    def readReg(self, addr):
        x = self.getVals(addr, 2)
        print hex(addr), hex(x[0] | x[1] << 8)

    def getVals(self, addr, bytes):
        vals = self.I2C.readBulk(self.ADDRESS, addr, bytes)
        return vals

    def getRaw(self):
        vals = self.getVals(self.source, 3)
        if vals:
            if len(vals) == 3:
                return [(((vals[1] & 127) << 8) + vals[0]) * 0.02 - 0.01 - 273.15]
            else:
                return False

        else:
            return False

    def getObjectTemperature(self):
        self.source = self.OBJADDR
        val = self.getRaw()
        if val:
            return val[0]
        else:
            return False

    def getAmbientTemperature(self):
        self.source = self.AMBADDR
        val = self.getRaw()
        if val:
            return val[0]
        else:
            return False