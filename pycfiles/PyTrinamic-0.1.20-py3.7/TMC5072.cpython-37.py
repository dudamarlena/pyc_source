# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5072\TMC5072.py
# Compiled at: 2019-11-27 05:57:43
# Size of source mod 2**32: 2444 bytes
"""
Created on 20.09.2019

@author: JM
"""
import PyTrinamic.ic.TMC5072.TMC5072_register as TMC5072_register
import PyTrinamic.ic.TMC5072.TMC5072_register_variant as TMC5072_register_variant
import PyTrinamic.ic.TMC5072.TMC5072_fields as TMC5072_fields
from PyTrinamic.helpers import TMC_helpers

class TMC5072:
    __doc__ = '\n    Class for the TMC5072 IC\n    '

    def __init__(self, channel):
        self._TMC5072__channel = channel
        self.registers = TMC5072_register
        self.fields = TMC5072_fields
        self.variants = TMC5072_register_variant
        self.MOTORS = 2

    def showChipInfo(self):
        print('TMC5072 chip info: The TMC5072 is a dual high performance stepper motor controller and driver IC with serial communication interfaces. Voltage supply: 4,75 - 26V')

    def writeRegister(self, registerAddress, value, channel):
        raise NotImplementedError

    def readRegister(self, registerAddress, channel):
        raise NotImplementedError

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC5072__channel), field[1], field[2], value), self._TMC5072__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC5072__channel), field[1], field[2])

    def rotate(self, motor, value):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        else:
            self.writeRegister(self.registers.AMAX[motor], 1000, self._TMC5072__channel)
            if value >= 0:
                self.writeRegister(self.registers.VMAX[motor], value, self._TMC5072__channel)
                self.writeRegister(self.registers.RAMPMODE[motor], 1, self._TMC5072__channel)
            else:
                self.writeRegister(self.registers.VMAX[motor], -value, self._TMC5072__channel)
                self.writeRegister(self.registers.RAMPMODE[motor], 2, self._TMC5072__channel)

    def stop(self, motor):
        self.rotate(motor, 0)

    def moveTo(self, motor, position, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        self.writeRegister(self.registers.RAMPMODE[motor], 0, self._TMC5072__channel)
        if velocity != 0:
            self.writeRegister(self.registers.VMAX[motor], velocity, self._TMC5072__channel)
        self.writeRegister(self.registers.XTARGET[motor], position, self._TMC5072__channel)