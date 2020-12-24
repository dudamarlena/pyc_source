# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/SENSORS/HMC5883L.py
# Compiled at: 2015-07-23 04:44:52
from numpy import int16

class HMC5883L:
    CONFA = 0
    CONFB = 1
    MODE = 2
    STATUS = 9
    samplesToAverage = 0
    samplesToAverage_choices = [1, 2, 4, 8]
    dataOutputRate = 6
    dataOutputRate_choices = [0.75, 1.5, 3, 7.5, 15, 30, 75]
    measurementConf = 0
    gainValue = 7
    gain_choices = [8, 7, 6, 5, 4, 3, 2, 1]
    scaling = [1370.0, 1090.0, 820.0, 660.0, 440.0, 390.0, 330.0, 230.0]
    params = {'init': ['Now'], 'setSamplesToAverage': samplesToAverage_choices, 
       'setDataOutputRate': dataOutputRate_choices, 
       'setGain': gain_choices}
    NUMPLOTS = 3

    def __init__(self, I2C):
        self.I2C = I2C
        self.ADDRESS = 30
        self.name = 'Magnetometer'
        self.init('')

    def init(self, dummy_variable_to_circumvent_framework_limitation):
        self.__writeCONFA__()
        self.__writeCONFB__()
        self.I2C.writeBulk(self.ADDRESS, [self.MODE, 0])

    def __writeCONFB__(self):
        self.I2C.writeBulk(self.ADDRESS, [self.CONFB, self.gainValue << 5])

    def __writeCONFA__(self):
        self.I2C.writeBulk(self.ADDRESS, [self.CONFA, self.dataOutputRate << 2 | self.samplesToAverage << 5 | self.measurementConf])

    def setSamplesToAverage(self, num):
        self.samplesToAverage = self.samplesToAverage_choices.index(num)
        self.__writeCONFA__()

    def setDataOutputRate(self, rate):
        self.dataOutputRate = self.dataOutputRate_choices.index(rate)
        self.__writeCONFA__()

    def setGain(self, gain):
        self.gainValue = self.gain_choices.index(gain)
        self.__writeCONFB__()

    def getVals(self, addr, bytes):
        vals = self.I2C.readBulk(self.ADDRESS, addr, bytes)
        return vals

    def getRaw(self):
        vals = self.getVals(3, 6)
        if vals:
            if len(vals) == 6:
                return [ int16(vals[(a * 2)] << 8 | vals[(a * 2 + 1)]) / self.scaling[self.gainValue] for a in range(3) ]
            else:
                return False

        else:
            return False