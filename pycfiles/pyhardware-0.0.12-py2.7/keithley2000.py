# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\serial\keithley2000.py
# Compiled at: 2013-10-05 04:00:20
import serial, sys, time
from pyhardware.drivers.serial import SerialDriver

class Keithley2000(SerialDriver):
    """
    Driver for the multimeter Keithley2000
    """
    _supported_models = [
     'Keithley2000']

    def __init__(self, *args):
        kwds = {'baudrate': 4800, 'bytesize': serial.EIGHTBITS, 
           'parity': serial.PARITY_NONE, 
           'stopbits': serial.STOPBITS_ONE, 
           'timeout': 0.5, 
           'xonxoff': True}
        super(Keithley2000, self).__init__(*args, **kwds)
        self.send('*IDN?')
        print 'DEVICE: ' + self.readline()
        self.send('*RST')
        self.send('*CLS')

    def doMeasurement(self, type='FRES', ch=1, mrange=99999, average=10, nplcycles=1, extracommand=''):
        self.measrange = mrange
        self.send('SYSTem:REMote')
        if self.ask('ROUTE:CLOSE:STATe?') != '(@)':
            self.send('ROUTe:OPEN:ALL')
        self.send('CONF:' + type + ' ' + str(mrange))
        self.send('SENSe:' + type + ':RANGE ' + str(mrange))
        self.send('ROUTE:CLOSE (@' + str(ch) + ')')
        self.send('SENSe:' + type + ':NPLCycles ' + str(nplcycles))
        self.send('SENSe:' + type + ':DIGITS MAXimum')
        self.send('SENSe:' + type + ':AVERage:TCONtrol REPeat')
        self.send('SENSe:' + type + ':AVERage:COUNt ' + str(average))
        self.send('SENSe:' + type + ':AVERage:STATe ON')
        self.send('TRIGGER:SOURCe IMMediate')
        self.send('TRIGGER:DELay:AUTO ON')
        self.send(extracommand)
        res = None
        for i in range(100):
            try:
                res = self.getValue(average * nplcycles * 0.02 * 1 + 0.2)
                break
            except ValueError:
                pass

        if res is None:
            raise ValueError('No value returned in time')
        self.send('ROUTe:OPEN:ALL')
        self.send('*CLS')
        self.send('SYST:LOCAL')
        return res

    def doFresMeasurement(self, ch=1, mrange=99999, average=10, nplcycles=1, extracommand=''):
        return self.doMeasurement(type='FRES', ch=ch, mrange=mrange, average=average, nplcycles=nplcycles, extracommand=extracommand)

    def doResMeasurement(self, ch=3, mrange=99999, average=10, nplcycles=1, extracommand=''):
        return self.doMeasurement(type='RES', ch=ch, mrange=mrange, average=average, nplcycles=nplcycles, extracommand=extracommand)

    def getValue(self, sleeptime=0.1):
        self.send('READ?')
        time.sleep(sleeptime)
        res = self.readline()
        return float(res.strip())

    def frontswitch(self):
        state = self.ask('SYSTem:FRSWitch?')
        if state == '1':
            return 'front'
        else:
            if state == '0':
                return 'back'
            return 'unknown'


if __name__ == '__main__':
    ea = Keithley2000(sys.argv[1])