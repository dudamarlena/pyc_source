# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC2100\TMC2100.py
# Compiled at: 2019-12-02 04:54:08
# Size of source mod 2**32: 1692 bytes
"""
Created on 15.10.2019

@author: JM
"""
import PyTrinamic.ic.TMC2100.TMC2100_register as TMC2100_register
import PyTrinamic.ic.TMC2100.TMC2100_register_variant as TMC2100_register_variant
import PyTrinamic.ic.TMC2100.TMC2100_fields as TMC2100_fields
from PyTrinamic.helpers import TMC_helpers

class TMC2100:
    __doc__ = '\n    Class for the TMC2100 IC\n    '

    def __init__(self, channel):
        self._TMC2100__channel = channel
        self.registers = TMC2100_register
        self.fields = TMC2100_fields
        self.variants = TMC2100_register_variant
        self.MOTORS = 2

    def showChipInfo(self):
        print('TMC2100 chip info: The TMC2100 is a standalone driver IC for two-phase stepper motors. Voltage supply: 4.75 - 46V')

    def writeRegister(self, registerAddress, value, channel):
        raise NotImplementedError

    def readRegister(self, registerAddress, channel):
        raise NotImplementedError

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC2100__channel), field[1], field[2], value), self._TMC2100__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC2100__channel), field[1], field[2])

    def moveBy(self, motor, distance, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        position = self.readRegister((self.registers.XACTUAL), (self._TMC2100__channel), signed=True)
        self.moveTo(motor, position + distance, velocity)
        return position + distance

    def get_pin_state(self):
        pass