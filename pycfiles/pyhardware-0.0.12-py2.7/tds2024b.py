# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\visa\tds2024b.py
# Compiled at: 2013-10-05 04:00:20
"""module to interface the TDS2024b scope (using VISA interface)"""
from pyhardware.drivers.visa import VisaDriver
from pandas import Series
import visa

class TDS2024B(VisaDriver):
    _supported_models = [
     'TDS 2024B']

    def easy_waveform(self, ch=1):
        self.write('DATa:WIDth 1')
        self.write('DATa:ENCdg RPBinary')
        self.write('DATa:STARt 1')
        self.write('DATa:STOP 2500')
        self.write('SELect:CH%i ON' % ch)
        self.write('DATa:SOUrce CH%i' % ch)
        self.write('WFRMPre:PT_Fmt Y')
        YZEro = float(self.ask('WFMPRe:YZEro?'))
        YMUlt = float(self.ask('WFMPRe:YMUlt?'))
        YOFf = float(self.ask('WFMPRe:YOFf?'))
        XZEro = float(self.ask('WFMPRe:XZEro?'))
        XINcr = float(self.ask('WFMPRe:XINcr?'))
        PT_OFf = float(self.ask('WFMPRe:PT_OFf?'))
        NR_Pt = int(self.ask('WFMPRe:NR_Pt?'))
        preamble = self.ask('WFMPRe?')
        print preamble
        rawdata = map(ord, tuple(self.ask('CURVe?')[-NR_Pt:]))
        tcol = XZEro + XINcr * (Series(range(NR_Pt)) - PT_OFf)
        trace = YZEro + YMUlt * (Series(rawdata, index=tcol) - YOFf)
        return trace


if __name__ == '__main__':
    ea = TDS2024B(sys.argv[1])