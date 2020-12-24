# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\evalboards\TMC6100_eval.py
# Compiled at: 2020-01-31 03:29:45
# Size of source mod 2**32: 1270 bytes
"""
Created on 31.01.2020

@author: JM
"""
import PyTrinamic.ic.TMC6100.TMC6100 as TMC6100
from PyTrinamic.helpers import TMC_helpers

class TMC6100_eval(TMC6100):

    def __init__(self, connection, moduleID=1):
        self.connection = connection
        TMC6100.__init__(self, connection=None, channel=moduleID)

    def register(self):
        return self.TMC6100.register()

    def variants(self):
        return self.TMC6100.variants()

    def maskShift(self):
        return self.TMC6100.maskShift()

    def ic(self):
        return self.TMC6100

    def writeRegister(self, registerAddress, value):
        return self.connection.writeDRV(registerAddress, value)

    def readRegister(self, registerAddress):
        return self.connection.readDRV(registerAddress)

    def writeRegisterField(self, registerAddress, value, mask, shift):
        return self.writeRegister(registerAddress, TMC_helpers.field_set(self.readRegister(registerAddress), mask, shift, value))

    def readRegisterField(self, registerAddress, mask, shift):
        return TMC_helpers.field_get(self.readRegister(registerAddress), mask, shift)


class _APs:
    pass