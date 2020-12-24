# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/achan.py
# Compiled at: 2015-08-18 13:16:49
import numpy as np
TEN_BIT = 10
TWELVE_BIT = 12
print 'LOADING'
gains = [1, 2, 4, 5, 8, 10, 16, 32]
allAnalogChannels = [
 'CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'I2V', 'V+', 'SEN', 'CAP', 'AN2', 'AN3', '5V']
multiplexedChannels = [
 'CH1', 'I2V', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'V+']
bipolars = ['CH1', 'I2V', 'CH3']
unipolars = ['CH4', 'CH5', 'CH6', 'CH7']
directInAnalogs = ['AN2', 'AN3', 'AN4', 'CAP', 'CAPCHARGE', 'SEN', '5V']
inputRanges = {'CH1': [16.5, -16.5], 'CH2': [
         16.5, -16.5], 
   'CH3': [
         -3.3, 3.3], 
   'I2V': [
         0.0033, -0.0033], 
   'V+': [
        0, 36.3], 
   'CH4': [
         0, 3.3], 
   'CH5': [0, 3.3], 'CH6': [0, 3.3], 'CH7': [0, 3.3], 'SEN': [
         0, 3.3], 
   'CAP': [0, 3.3], 'AN2': [0, 3.3], 'AN3': [0, 3.3], '5V': [0, 6.6]}
picADCMultiplex = {'CH2': 0}
for a in multiplexedChannels:
    picADCMultiplex[a] = 1

for a in directInAnalogs:
    picADCMultiplex[a] = directInAnalogs.index(a) + 2

class analogInputSource:
    gain_values = [
     1, 2, 4, 5, 8, 10, 16, 32]
    offsetEnabled = False
    gainEnabled = False
    offsetCode = None
    offset = 0.0
    gain = None
    gainPGA = None
    MAX_DACVAL = 4095
    multiplexSelection = None
    inverted = False
    inversion = 1.0
    calPoly10 = np.poly1d([0, 3.3 / 1023, 0.0])
    calPoly12 = np.poly1d([0, 3.3 / 4095, 0.0])
    calibrationReady = False
    defaultOffsetCode = 0

    def __init__(self, name, **args):
        self.name = name
        self.CHOSA = picADCMultiplex[self.name]
        self.adc_shifts = []
        self.polynomials = {}
        if name in multiplexedChannels:
            self.multiplexSelection = multiplexedChannels.index(name)
        self.R = inputRanges[name]
        if self.R[1] - self.R[0] < 0:
            self.inverted = True
            self.inversion = -1
        self.scaling = 1.0
        if name == 'CH2':
            self.gainEnabled = True
            self.gainPGA = 2
            self.gain = 0
        elif name in multiplexedChannels:
            self.gainEnabled = True
            self.offsetEnabled = True
            self.offsetCode = 0
            self.defaultOffsetCode = 0
            self.gainPGA = 1
            self.gain = 0
            if name in bipolars:
                self.defaultOffsetCode = int(self.MAX_DACVAL / 2)
                self.offsetCode = self.defaultOffsetCode
        self.gain = 0
        self.regenerateCalibration()

    def getOffset(self):
        if self.offsetCode == None:
            return 0
        else:
            return self.offsetCode * (self.R[1] - self.R[0]) / 4095.0 + self.R[0]

    def setOffset(self, offset):
        if not self.offsetEnabled:
            print 'Offset selection is not available on', self.name
            return False
        if not min(self.R) <= offset <= max(self.R):
            print 'Offset out of range ', self.R
            return False
        self.offsetCode = int(4095 * (offset - self.R[0]) / (self.R[1] - self.R[0]))
        print 'setting offset', offset, self.offsetCode
        self.offset = offset
        self.regenerateCalibration()

    def setGain(self, g):
        if not self.gainEnabled:
            print 'Analog gain is not available on', self.name
            return False
        self.gain = self.gain_values.index(g)
        self.regenerateCalibration()

    def inRange(self, val):
        v = self.voltToCode12(val)
        return v >= 0 and v <= 4095

    def __conservativeInRange__(self, val):
        v = self.voltToCode12(val)
        return v >= 50 and v <= 4000

    def loadCalibrationTable(self, table):
        self.adc_shifts = np.array(table)

    def loadPolynomials(self, polys):
        for a in range(len(polys)):
            epoly = [ float(b) for b in polys[a] ]
            self.polynomials[a] = np.poly1d(epoly)

    def regenerateCalibration(self):
        B = self.R[1]
        A = self.R[0]
        intercept = self.R[0]
        offset = self.getOffset()
        if self.gain != None:
            gain = self.gain_values[self.gain]
            B = offset + 1.0 * (B - offset) / gain
            A = offset + 1.0 * (A - offset) / gain
        slope = B - A
        intercept = A
        if self.calibrationReady and (self.offsetCode == self.defaultOffsetCode or self.offsetEnabled == False):
            self.calPoly10 = self.__cal10__
            self.calPoly12 = self.__cal12__
        else:
            self.calPoly10 = np.poly1d([0, slope / 1023.0, intercept])
            self.calPoly12 = np.poly1d([0, slope / 4095.0, intercept])
        self.voltToCode10 = np.poly1d([0, 1023.0 / slope, -1023 * intercept / slope])
        self.voltToCode12 = np.poly1d([0, 4095.0 / slope, -4095 * intercept / slope])
        return

    def __cal12__(self, RAW):
        avg_shifts = (self.adc_shifts[np.int16(np.floor(RAW))] + self.adc_shifts[np.int16(np.ceil(RAW))]) / 2.0
        RAW = RAW - 4095 * (avg_shifts / 25000.0 - 0.004) / 3.3
        return self.polynomials[self.gain](RAW)

    def __cal10__(self, RAW):
        RAW *= 4095 / 1023.0
        avg_shifts = (self.adc_shifts[np.int16(np.floor(RAW))] + self.adc_shifts[np.int16(np.ceil(RAW))]) / 2.0
        RAW = RAW - 4095 * (avg_shifts / 25000.0 - 0.004) / 3.3
        return self.polynomials[self.gain](RAW)


class analogAcquisitionChannel:
    """
        This class takes care of oscilloscope data fetched from the device.
        Each instance may be linked to a particular input.
        Since only up to two channels may be captured at a time with the vLabtool, only two instances will be required
        
        Each instance will be linked to a particular inputSource instance by the capture routines.
        When data is requested , it will return after applying calibration and gain details
        stored in the selected inputSource
        """

    def __init__(self, a):
        self.name = ''
        self.gain = 0
        self.channel = a
        self.channel_names = ['CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'I2V', '5V', 'PCS', '9V', 'IN1', 'SEN', 'TEMP']
        self.calibration_ref196 = 1.0
        self.resolution = TEN_BIT
        self.xaxis = np.zeros(10000)
        self.yaxis = np.zeros(10000)
        self.length = 100
        self.timebase = 1.0
        self.source = analogInputSource('CH1')

    def fix_value(self, val):
        if self.resolution == TWELVE_BIT:
            return self.calibration_ref196 * self.source.calPoly12(val)
        else:
            return self.calibration_ref196 * self.source.calPoly10(val)

    def set_yval(self, pos, val):
        self.yaxis[pos] = self.fix_value(val)

    def set_xval(self, pos, val):
        self.xaxis[pos] = val

    def set_params(self, **keys):
        self.gain = keys.get('gain', self.gain)
        self.name = keys.get('channel', self.channel)
        self.source = keys.get('source', self.source)
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