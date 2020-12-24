# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5161\TMC5161.py
# Compiled at: 2020-01-30 03:37:30
# Size of source mod 2**32: 1736 bytes
"""
Created on 30.01.2020

@author: JM
"""
import PyTrinamic.ic.TMC5161.TMC5161_register as TMC5161_register
import PyTrinamic.ic.TMC5161.TMC5161_register_variant as TMC5161_register_variant
import PyTrinamic.ic.TMC5161.TMC5161_fields as TMC5161_fields
from PyTrinamic.helpers import TMC_helpers

class TMC5161:
    __doc__ = '\n    Class for the TMC5161 IC\n    '

    def __init__(self, channel):
        self._TMC5161__channel = channel
        self.registers = TMC5161_register
        self.fields = TMC5161_fields
        self.variants = TMC5161_register_variant
        self.MOTORS = 2

    def showChipInfo(self):
        print('TMC5161 chip info: The TMC5161 is a high-power two phase stepper motor controller and driver IC with serial communication interfaces. Voltage supply: 8 - 55V')

    def writeRegister(self, registerAddress, value, channel):
        raise NotImplementedError

    def readRegister(self, registerAddress, channel):
        raise NotImplementedError

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC5161__channel), field[1], field[2], value), self._TMC5161__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC5161__channel), field[1], field[2])

    def moveBy(self, motor, distance, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        position = self.readRegister((self.registers.XACTUAL), (self._TMC5161__channel), signed=True)
        self.moveTo(motor, position + distance, velocity)
        return position + distance

    def get_pin_state(self):
        pass