# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/ic/series_7400_1.py
# Compiled at: 2014-03-16 17:41:12
from BinPy import *

class IC_7400(LC):

    def __init__(self, name):
        LC.__init__(self, name)
        self.pin1 = Connector(self, 'pin1')
        self.pin2 = Connector(self, 'pin2')
        self.pin3 = Connector(self, 'pin3')
        self.pin4 = Connector(self, 'pin4')
        self.pin5 = Connector(self, 'pin5')
        self.pin6 = Connector(self, 'pin6')
        self.pin7 = Connector(self, 'pin7')
        self.pin8 = Connector(self, 'pin8')
        self.pin9 = Connector(self, 'pin9')
        self.pin10 = Connector(self, 'pin10')
        self.pin11 = Connector(self, 'pin11')
        self.pin12 = Connector(self, 'pin12')
        self.pin13 = Connector(self, 'pin13')
        self.pin14 = Connector(self, 'pin14')
        NAND1 = Nand('NAND1')
        NAND2 = Nand('NAND2')
        NAND3 = Nand('NAND3')
        NAND4 = Nand('NAND4')
        self.pin1.connect(NAND1.A)
        self.pin2.connect(NAND1.B)
        NAND1.C.connect(self.pin3)
        self.pin4.connect(NAND2.A)
        self.pin5.connect(NAND2.B)
        NAND1.C.connect(self.pin6)
        self.pin10.connect(NAND3.A)
        self.pin9.connect(NAND3.B)
        NAND1.C.connect(self.pin8)
        self.pin13.connect(NAND4.A)
        self.pin12.connect(NAND4.B)
        NAND1.C.connect(self.pin11)