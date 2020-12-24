# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5130\TMC5130.py
# Compiled at: 2019-11-27 06:00:08
# Size of source mod 2**32: 2748 bytes
"""
Created on 02.01.2019

@author: ed
"""
import PyTrinamic.ic.TMC5130.TMC5130_register as TMC5130_register
import PyTrinamic.ic.TMC5130.TMC5130_register_variant as TMC5130_register_variant
import PyTrinamic.ic.TMC5130.TMC5130_fields as TMC5130_fields
from PyTrinamic.helpers import TMC_helpers

class TMC5130:
    __doc__ = '\n    Class for the TMC5130 IC\n    '

    def __init__(self, channel):
        self._TMC5130__channel = channel
        self.registers = TMC5130_register
        self.fields = TMC5130_fields
        self.variants = TMC5130_register_variant
        self.MOTORS = 2

    def showChipInfo(self):
        print('TMC5130 chip info: The TMC5130/A is a high-performance stepper motor controller and driver IC with serial communication interfaces. Voltage supply: 4,75 - 46V')

    def writeRegister(self, registerAddress, value, channel):
        raise NotImplementedError

    def readRegister(self, registerAddress, channel):
        raise NotImplementedError

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC5130__channel), field[1], field[2], value), self._TMC5130__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC5130__channel), field[1], field[2])

    def rotate(self, motor, value):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        else:
            self.writeRegister(self.registers.AMAX, 1000, self._TMC5130__channel)
            if value >= 0:
                self.writeRegister(self.registers.VMAX, value, self._TMC5130__channel)
                self.writeRegister(self.registers.RAMPMODE, 1, self._TMC5130__channel)
            else:
                self.writeRegister(self.registers.VMAX, -value, self._TMC5130__channel)
                self.writeRegister(self.registers.RAMPMODE, 2, self._TMC5130__channel)

    def stop(self, motor):
        self.rotate(motor, 0)

    def moveTo(self, motor, position, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        self.writeRegister(self.registers.RAMPMODE, 0, self._TMC5130__channel)
        if velocity != 0:
            self.writeRegister(self.registers.VMAX, velocity, self._TMC5130__channel)
        self.writeRegister(self.registers.XTARGET, position, self._TMC5130__channel)

    def moveBy(self, motor, distance, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        position = self.readRegister((self.registers.XACTUAL), (self._TMC5130__channel), signed=True)
        self.moveTo(motor, position + distance, velocity)
        return position + distance

    def get_pin_state(self):
        pass