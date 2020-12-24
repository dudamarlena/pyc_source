# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/SENSORS/TSL2561.py
# Compiled at: 2015-07-23 10:05:14
"""
Adapted from https://github.com/janheise/TSL2561
"""
import time

class TSL2561:
    VISIBLE = 2
    INFRARED = 1
    FULLSPECTRUM = 0
    READBIT = 1
    COMMAND_BIT = 128
    CONTROL_POWERON = 3
    CONTROL_POWEROFF = 0
    REGISTER_CONTROL = 0
    REGISTER_TIMING = 1
    REGISTER_ID = 10
    INTEGRATIONTIME_13MS = 0
    INTEGRATIONTIME_101MS = 1
    INTEGRATIONTIME_402MS = 2
    GAIN_1X = 0
    GAIN_16X = 16
    ADDRESS = 57
    timing = INTEGRATIONTIME_13MS
    gain = GAIN_16X
    name = 'TSL2561 Luminosity'
    NUMPLOTS = 3

    def __init__(self, I2C, **args):
        self.ADDRESS = args.get('address', 57)
        self.I2C = I2C
        self.enable()
        self.wait()
        self.I2C.writeBulk(self.ADDRESS, [129, 17])
        infra = self.I2C.readBulk(self.ADDRESS, 174, 2)
        full = self.I2C.readBulk(self.ADDRESS, 172, 2)
        full = full[1] << 8 | full[0]
        infra = infra[1] << 8 | infra[0]
        print 'Full:     %04x' % full
        print 'Infrared: %04x' % infra
        print 'Visible:  %04x' % (full - infra)
        self.params = {'setGain': ['1x', '16x'], 'setTiming': [0, 1, 2]}

    def getID(self):
        ID = self.I2C.readBulk(self.ADDRESS, self.REGISTER_ID, 1)
        print hex(ID)
        return ID

    def getRaw(self):
        infra = self.I2C.readBulk(self.ADDRESS, 174, 2)
        full = self.I2C.readBulk(self.ADDRESS, 172, 2)
        if infra and full:
            full = full[1] << 8 | full[0]
            infra = infra[1] << 8 | infra[0]
            return [
             full, infra, full - infra]
        else:
            return False

    def setGain(self, gain):
        if gain == '1x':
            self.gain = self.GAIN_1X
        elif gain == '16x':
            self.gain = self.GAIN_16X
        else:
            self.gain = self.GAIN_0X
        self.I2C.writeBulk(self.ADDRESS, [self.COMMAND_BIT | self.REGISTER_TIMING, self.gain | self.timing])

    def setTiming(self, timing):
        print [
         13, 101, 402][timing], 'mS'
        self.timing = timing
        self.I2C.writeBulk(self.ADDRESS, [self.COMMAND_BIT | self.REGISTER_TIMING, self.gain | self.timing])

    def enable(self):
        self.I2C.writeBulk(self.ADDRESS, [self.COMMAND_BIT | self.REGISTER_CONTROL, self.CONTROL_POWERON])

    def disable(self):
        self.I2C.writeBulk(self.ADDRESS, [self.COMMAND_BIT | self.REGISTER_CONTROL, self.CONTROL_POWEROFF])

    def wait(self):
        if self.timing == self.INTEGRATIONTIME_13MS:
            time.sleep(0.14)
        if self.timing == self.INTEGRATIONTIME_101MS:
            time.sleep(0.102)
        if self.timing == self.INTEGRATIONTIME_402MS:
            time.sleep(0.403)