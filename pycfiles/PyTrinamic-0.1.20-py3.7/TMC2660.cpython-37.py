# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC2660\TMC2660.py
# Compiled at: 2019-11-27 05:39:34
# Size of source mod 2**32: 1361 bytes
"""
Created on 07.11.2019

@author: JM
"""
import PyTrinamic.ic.TMC2660.TMC2660_register as TMC2660_register
import PyTrinamic.ic.TMC2660.TMC2660_register_variant as TMC2660_register_variant
import PyTrinamic.ic.TMC2660.TMC2660_fields as TMC2660_fields
from PyTrinamic.helpers import TMC_helpers

class TMC2660:
    __doc__ = '\n    Class for the TMC2660 IC\n    '

    def __init__(self, channel):
        self._TMC2660__channel = channel
        self.registers = TMC2660_register
        self.fields = TMC2660_fields
        self.variants = TMC2660_register_variant
        self.MOTORS = 2

    def showChipInfo(self):
        print('TMC2660 chip info: The TMC2660 is a driver for two-phase stepper motors. Voltage supply: up to 30V ')

    def writeRegister(self, registerAddress, value, channel):
        raise NotImplementedError

    def readRegister(self, registerAddress, channel):
        raise NotImplementedError

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC2660__channel), field[1], field[2], value), self._TMC2660__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC2660__channel), field[1], field[2])

    def get_pin_state(self):
        pass