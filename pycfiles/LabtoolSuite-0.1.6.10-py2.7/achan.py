# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Labtools/achan.py
# Compiled at: 2015-05-24 08:28:04
import numpy as np
TEN_BIT = 10
TWELVE_BIT = 12
gains = [
 1, 2, 4, 5, 8, 10, 16, 32]
calfacs = {}
try:
    from calib_data import calibs
    for A in calibs.calibs:
        calfacs[A] = [ np.poly1d(B) for B in calibs.calibs[A] ]

except:
    print 'Loading default calibration values'
    for n in range(4):
        calfacs['CH' + str(n + 1)] = [ np.poly1d([0, -33 / 1023.0 / gains[a], 16.5 / gains[a]]) for a in range(8) ]

    for n in ['CH5', 'CH6', 'CH7', 'CH8', 'CH9']:
        calfacs[n] = [ np.poly1d([0, 3.3 / 1023.0 / gains[a], 0]) for a in range(8) ]

calfacs['5V'] = [ np.poly1d([0, 6.6 / 1023.0 / gains[a], 0]) for a in range(8) ]
calfacs['PCS'] = [ np.poly1d([0, 3.3 / 1023.0 / gains[a], 0]) for a in range(8) ]
calfacs['9V'] = [ np.poly1d([0, 33 / 1023.0 / gains[a], 0]) for a in range(8) ]
calfacs['IN1'] = [
 np.poly1d([0, 3.3 / 1023.0, 0])]
calfacs['SEN'] = [np.poly1d([0, 3.3 / 1023.0, 0])]
calfacs['TEMP'] = [np.poly1d([0, 3.3 / 1023.0, 0])]

class analog_channel:

    def __init__(self, a):
        self.name = ''
        self.gain = 0
        self.channel = a
        self.channel_names = ['CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', 'CH9', '5V', 'PCS', '9V', 'IN1', 'SEN', 'TEMP']
        self.calibration_ref196 = 1.0
        self.resolution = TEN_BIT
        self.xaxis = np.zeros(4000)
        self.yaxis = np.zeros(4000)
        self.length = 100
        self.timebase = 1.0

    def fix_value(self, val):
        if self.channel_names.index(self.name) > 11:
            self.gain = 0
        if self.resolution == TWELVE_BIT:
            return self.calibration_ref196 * calfacs[self.name][self.gain](val / 4.0)
        else:
            return self.calibration_ref196 * calfacs[self.name][self.gain](val)

    def set_yval(self, pos, val):
        self.yaxis[pos] = self.fix_value(val)

    def set_xval(self, pos, val):
        self.xaxis[pos] = val

    def set_params(self, **keys):
        self.gain = keys.get('gain', self.gain)
        self.name = keys.get('channel', self.channel)
        self.resolution = keys.get('resolution', self.resolution)
        l = keys.get('length', self.length)
        t = keys.get('timebase', self.timebase)
        if t != self.timebase or l != self.length:
            self.timebase = t
            self.length = l
            self.regenerate_xaxis()

    def regenerate_xaxis(self):
        for a in range(self.length):
            self.xaxis[a] = self.timebase * a

    def get_xaxis(self):
        return self.xaxis[:self.length]

    def get_yaxis(self):
        return self.yaxis[:self.length]