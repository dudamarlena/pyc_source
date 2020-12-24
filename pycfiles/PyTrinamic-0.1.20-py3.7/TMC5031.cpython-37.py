# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5031\TMC5031.py
# Compiled at: 2020-01-29 09:37:44
# Size of source mod 2**32: 2441 bytes
"""
Created on 29.01.2020

@author: JM
"""
import PyTrinamic.ic.TMC5031.TMC5031_register as TMC5031_register
import PyTrinamic.ic.TMC5031.TMC5031_register_variant as TMC5031_register_variant
import PyTrinamic.ic.TMC5031.TMC5031_fields as TMC5031_fields
from PyTrinamic.helpers import TMC_helpers

class TMC5031:
    __doc__ = '\n    Class for the TMC5031 IC\n    '

    def __init__(self, channel):
        self._TMC5031__channel = channel
        self.registers = TMC5031_register
        self.fields = TMC5031_fields
        self.variants = TMC5031_register_variant
        self.MOTORS = 2

    def showChipInfo(self):
        print('TMC5031 chip info: The TMC5031 is a cost-effective dual stepper motor controller and driver IC with serial communication interface. Voltage supply: 4,75 - 16V')

    def writeRegister(self, registerAddress, value, channel):
        raise NotImplementedError

    def readRegister(self, registerAddress, channel):
        raise NotImplementedError

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC5031__channel), field[1], field[2], value), self._TMC5031__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC5031__channel), field[1], field[2])

    def rotate(self, motor, value):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        else:
            self.writeRegister(self.registers.AMAX[motor], 1000, self._TMC5031__channel)
            if value >= 0:
                self.writeRegister(self.registers.VMAX[motor], value, self._TMC5031__channel)
                self.writeRegister(self.registers.RAMPMODE[motor], 1, self._TMC5031__channel)
            else:
                self.writeRegister(self.registers.VMAX[motor], -value, self._TMC5031__channel)
                self.writeRegister(self.registers.RAMPMODE[motor], 2, self._TMC5031__channel)

    def stop(self, motor):
        self.rotate(motor, 0)

    def moveTo(self, motor, position, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        self.writeRegister(self.registers.RAMPMODE[motor], 0, self._TMC5031__channel)
        if velocity != 0:
            self.writeRegister(self.registers.VMAX[motor], velocity, self._TMC5031__channel)
        self.writeRegister(self.registers.XTARGET[motor], position, self._TMC5031__channel)