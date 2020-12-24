# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\serial\agilent34401a.py
# Compiled at: 2013-10-09 11:09:05
import serial, sys, time
from pyhardware.drivers.serial import SerialDriver

class Agilent34401A(SerialDriver):
    _supported_models = [
     '34401A']
    measrange = 100000

    def __init__(self, *args, **kwds):
        kwds = {'baudrate': 9600, 'bytesize': serial.SEVENBITS, 
           'parity': serial.PARITY_EVEN, 
           'stopbits': serial.STOPBITS_TWO, 
           'timeout': 0.5, 
           'dsrdtr': True}
        super(Agilent34401A, self).__init__(*args, **kwds)
        self.send('*IDN?')
        print 'DEVICE: ' + self.ser.readline()
        self.send('*RST')
        self.send('*CLS')

    def setResistanceMeasurement(self, mrange=100000):
        self.measrange = mrange
        self.send('SYSTem:REMote')
        self.send('DISPLAY:TEXT "Measuring..." ')
        self.send('CONF:FRES ' + str(self.measrange))
        self.send('TRIGGER:SOURCe IMMediate')
        self.send('TRIGGER:DELay:AUTO ON')

    def endResistanceMeasurement(self):
        self.send('DISPLAY:TEXT:CLEAR')
        self.send('*CLS')
        self.send('SYST:LOCAL')

    def getValue(self):
        self.send('READ?')
        time.sleep(0.1)
        res = self.ser.readline()
        print 'Resistance = ' + res
        return float(res.strip())


if __name__ == '__main__':
    ea = Agilent34401A(sys.argv[1])