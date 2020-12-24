# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5041\TMC5041.py
# Compiled at: 2019-11-27 05:46:03
# Size of source mod 2**32: 2441 bytes
"""
Created on 18.04.2019

@author: LH
"""
import PyTrinamic.ic.TMC5041.TMC5041_register as TMC5041_register
import PyTrinamic.ic.TMC5041.TMC5041_register_variant as TMC5041_register_variant
import PyTrinamic.ic.TMC5041.TMC5041_fields as TMC5041_fields
from PyTrinamic.helpers import TMC_helpers

class TMC5041:
    __doc__ = '\n    Class for the TMC5041 IC\n    '

    def __init__(self, channel):
        self._TMC5041__channel = channel
        self.registers = TMC5041_register
        self.fields = TMC5041_fields
        self.variants = TMC5041_register_variant
        self.MOTORS = 2

    def showChipInfo(self):
        print('TMC5041 chip info: The TMC5041 is a cost-effective dual stepper motor controller and driver IC with serial communication interface. Voltage supply: 4,75 - 26V')

    def writeRegister(self, registerAddress, value, channel):
        raise NotImplementedError

    def readRegister(self, registerAddress, channel):
        raise NotImplementedError

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC5041__channel), field[1], field[2], value), self._TMC5041__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC5041__channel), field[1], field[2])

    def rotate(self, motor, value):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        else:
            self.writeRegister(self.registers.AMAX[motor], 1000, self._TMC5041__channel)
            if value >= 0:
                self.writeRegister(self.registers.VMAX[motor], value, self._TMC5041__channel)
                self.writeRegister(self.registers.RAMPMODE[motor], 1, self._TMC5041__channel)
            else:
                self.writeRegister(self.registers.VMAX[motor], -value, self._TMC5041__channel)
                self.writeRegister(self.registers.RAMPMODE[motor], 2, self._TMC5041__channel)

    def stop(self, motor):
        self.rotate(motor, 0)

    def moveTo(self, motor, position, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        self.writeRegister(self.registers.RAMPMODE[motor], 0, self._TMC5041__channel)
        if velocity != 0:
            self.writeRegister(self.registers.VMAX[motor], velocity, self._TMC5041__channel)
        self.writeRegister(self.registers.XTARGET[motor], position, self._TMC5041__channel)