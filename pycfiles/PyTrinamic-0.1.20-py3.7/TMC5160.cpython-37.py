# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5160\TMC5160.py
# Compiled at: 2019-11-27 06:03:23
# Size of source mod 2**32: 1728 bytes
"""
Created on 24.10.2019

@author: JM
"""
import PyTrinamic.ic.TMC5160.TMC5160_register as TMC5160_register
import PyTrinamic.ic.TMC5160.TMC5160_register_variant as TMC5160_register_variant
import PyTrinamic.ic.TMC5160.TMC5160_fields as TMC5160_fields
from PyTrinamic.helpers import TMC_helpers

class TMC5160:
    __doc__ = '\n    Class for the TMC5160 IC\n    '

    def __init__(self, channel):
        self._TMC5160__channel = channel
        self.registers = TMC5160_register
        self.fields = TMC5160_fields
        self.variants = TMC5160_register_variant
        self.MOTORS = 2

    def showChipInfo(self):
        print('TMC5160 chip info: The TMC5160/A is a high-power stepper motor controller and driver IC with serial communication interfaces. Voltage supply: 8 - 60V')

    def writeRegister(self, registerAddress, value, channel):
        raise NotImplementedError

    def readRegister(self, registerAddress, channel):
        raise NotImplementedError

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC5160__channel), field[1], field[2], value), self._TMC5160__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC5160__channel), field[1], field[2])

    def moveBy(self, motor, distance, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        position = self.readRegister((self.registers.XACTUAL), (self._TMC5160__channel), signed=True)
        self.moveTo(motor, position + distance, velocity)
        return position + distance

    def get_pin_state(self):
        pass