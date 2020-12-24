# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/SENSORS/SHT21.py
# Compiled at: 2015-07-23 04:44:50
from numpy import int16
import time

class SHT21:
    RESET = 254
    TEMP_ADDRESS = 243
    HUMIDITY_ADDRESS = 245
    selected = 243
    NUMPLOTS = 1

    def __init__(self, I2C, **args):
        self.I2C = I2C
        self.ADDRESS = args.get('address', 64)
        self.name = 'Humidity/Temperature'
        self.params = {'selectParameter': ['temperature', 'humidity']}
        self.init('')

    def init(self, x):
        self.I2C.writeBulk(self.ADDRESS, [self.RESET])
        time.sleep(0.1)

    def rawToTemp(self, vals):
        if vals:
            if len(vals):
                v = vals[0] << 8 | vals[1] & 252
                v *= 175.72
                v /= 65536
                v -= 46.85
                return [
                 v]
        return False

    def rawToRH(self, vals):
        if vals:
            if len(vals):
                v = vals[0] << 8 | vals[1] & 252
                v *= 125.0
                v /= 65536
                v -= 6
                return [
                 v]
        return False

    @staticmethod
    def _calculate_checksum(data, number_of_bytes):
        """5.7 CRC Checksum using the polynomial given in the datasheet
                Credits: https://github.com/jaques/sht21_python/blob/master/sht21.py
                """
        POLYNOMIAL = 305
        crc = 0
        for byteCtr in range(number_of_bytes):
            crc ^= data[byteCtr]
            for bit in range(8, 0, -1):
                if crc & 128:
                    crc = crc << 1 ^ POLYNOMIAL
                else:
                    crc = crc << 1

        return crc

    def selectParameter(self, param):
        if param == 'temperature':
            self.selected = self.TEMP_ADDRESS
        elif param == 'humidity':
            self.selected = self.HUMIDITY_ADDRESS

    def getRaw(self):
        self.I2C.writeBulk(self.ADDRESS, [self.selected])
        if self.selected == self.TEMP_ADDRESS:
            time.sleep(0.1)
        else:
            if self.selected == self.HUMIDITY_ADDRESS:
                time.sleep(0.05)
            vals = self.I2C.simpleRead(self.ADDRESS, 3)
            if vals:
                if self._calculate_checksum(vals, 2) != vals[2]:
                    return False
                    print vals
            if self.selected == self.TEMP_ADDRESS:
                return self.rawToTemp(vals)
            if self.selected == self.HUMIDITY_ADDRESS:
                return self.rawToRH(vals)