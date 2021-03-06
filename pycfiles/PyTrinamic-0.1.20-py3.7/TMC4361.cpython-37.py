# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC4361\TMC4361.py
# Compiled at: 2019-12-20 05:08:25
# Size of source mod 2**32: 1687 bytes
"""
Created on 07.11.2019

@author: JM
"""
import PyTrinamic.ic.TMC4361.TMC4361_register as TMC4361_register
import PyTrinamic.ic.TMC4361.TMC4361_register_variant as TMC4361_register_variant
import PyTrinamic.ic.TMC4361.TMC4361_fields as TMC4361_fields
from PyTrinamic.helpers import TMC_helpers

class TMC4361:
    __doc__ = '\n    Class for the TMC4361 IC\n    '

    def __init__(self, channel):
        self._TMC4361__channel = channel
        self.registers = TMC4361_register
        self.fields = TMC4361_fields
        self.variants = TMC4361_register_variant
        self.MOTORS = 2

    def showChipInfo(self):
        print('TMC4361 chip info: The TMC4361 is a miniaturized high-performance motion controller for stepper motor drivers.')

    def writeRegister(self, registerAddress, value, channel):
        raise NotImplementedError

    def readRegister(self, registerAddress, channel):
        raise NotImplementedError

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC4361__channel), field[1], field[2], value), self._TMC4361__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC4361__channel), field[1], field[2])

    def moveBy(self, motor, distance, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        position = self.readRegister((self.registers.XACTUAL), (self._TMC4361__channel), signed=True)
        self.moveTo(motor, position + distance, velocity)
        return position + distance

    def get_pin_state(self):
        pass