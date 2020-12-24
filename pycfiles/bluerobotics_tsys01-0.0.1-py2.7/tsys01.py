# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/tsys01/tsys01.py
# Compiled at: 2018-12-11 09:03:48
try:
    import smbus
except:
    print 'Try sudo apt-get install python-smbus'

from time import sleep
UNITS_Centigrade = 1
UNITS_Farenheit = 2
UNITS_Kelvin = 3

class TSYS01(object):
    _TSYS01_ADDR = 119
    _TSYS01_PROM_READ = 160
    _TSYS01_RESET = 30
    _TSYS01_CONVERT = 72
    _TSYS01_READ = 0

    def __init__(self, bus=1):
        self._temperature = 0
        self._k = []
        try:
            self._bus = smbus.SMBus(bus)
        except:
            print 'Bus %d is not available.' % bus
            print 'Available busses are listed as /dev/i2c*'
            self._bus = None

        return

    def init(self):
        if self._bus is None:
            return False
        else:
            self._bus.write_byte(self._TSYS01_ADDR, self._TSYS01_RESET)
            sleep(0.1)
            self._k = []
            for prom in range(170, 160, -2):
                k = self._bus.read_word_data(self._TSYS01_ADDR, prom)
                k = (k & 255) << 8 | k >> 8
                self._k.append(k)

            return True

    def read(self):
        if self._bus is None:
            print 'No bus!'
            return False
        else:
            self._bus.write_byte(self._TSYS01_ADDR, self._TSYS01_CONVERT)
            sleep(0.01)
            adc = self._bus.read_i2c_block_data(self._TSYS01_ADDR, self._TSYS01_READ, 3)
            adc = adc[0] << 16 | adc[1] << 8 | adc[2]
            self._calculate(adc)
            return True

    def temperature(self, conversion=UNITS_Centigrade):
        if conversion == UNITS_Farenheit:
            return 9 / 5 * self._temperature + 32
        if conversion == UNITS_Kelvin:
            return self._temperature - 273
        return self._temperature

    def _calculate(self, adc):
        adc16 = adc / 256
        self._temperature = -2 * self._k[4] * 1e-21 * adc16 ** 4 + 4 * self._k[3] * 1e-16 * adc16 ** 3 + -2 * self._k[2] * 1e-11 * adc16 ** 2 + 1 * self._k[1] * 1e-06 * adc16 + -1.5 * self._k[0] * 0.01