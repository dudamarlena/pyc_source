# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\evalboards\TMC6200_eval.py
# Compiled at: 2019-12-05 04:44:55
# Size of source mod 2**32: 1300 bytes
"""
Created on 06.03.2019

@author: ED
"""
import PyTrinamic.ic.TMC6200.TMC6200 as TMC6200
from PyTrinamic.helpers import TMC_helpers

class TMC6200_eval(TMC6200):

    def __init__(self, connection, moduleID=1):
        self.connection = connection
        TMC6200.__init__(self, connection=None, channel=moduleID)

    def register(self):
        return self.tmc6200.register()

    def variants(self):
        return self.tmc6200.variants()

    def maskShift(self):
        return self.tmc6200.maskShift()

    def ic(self):
        return self.tmc6200

    def writeRegister(self, registerAddress, value):
        return self.connection.writeDRV(registerAddress, value)

    def readRegister(self, registerAddress):
        return self.connection.readDRV(registerAddress)

    def writeRegisterField(self, registerAddress, value, mask, shift):
        return self.writeRegister(registerAddress, TMC_helpers.field_set(self.readRegister(registerAddress), mask, shift, value))

    def readRegisterField(self, registerAddress, mask, shift):
        return TMC_helpers.field_get(self.readRegister(registerAddress), mask, shift)


class _APs:
    TargetPosition = 0