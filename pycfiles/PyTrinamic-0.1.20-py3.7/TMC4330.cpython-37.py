# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC4330\TMC4330.py
# Compiled at: 2020-02-06 07:42:26
# Size of source mod 2**32: 2296 bytes
"""
Created on 06.02.2020

@author: JM
"""
import struct
import PyTrinamic.ic.TMC4330.TMC4330_register as TMC4330_register
import PyTrinamic.ic.TMC4330.TMC4330_register_variant as TMC4330_register_variant
import PyTrinamic.ic.TMC4330.TMC4330_fields as TMC4330_fields
from PyTrinamic.helpers import TMC_helpers
DATAGRAM_FORMAT = '>BI'
DATAGRAM_LENGTH = 5

class TMC4330:
    __doc__ = '\n    Class for the TMC4330 IC\n    '

    def __init__(self, connection, channel=0):
        self._TMC4330__connection = connection
        self._TMC4330__channel = channel
        self.registers = TMC4330_register
        self.fields = TMC4330_fields
        self.variants = TMC4330_register_variant
        self.MOTORS = 1

    def showChipInfo(self):
        print('TMC4330 chip info: The TMC4330 is a miniaturized high-performance motion controller for stepper motor drivers, particulary designed for fast jerk-limited motion profile applications with a wide range of ramp profiles. Voltage supply: - ')

    def writeRegister(self, registerAddress, value):
        datagram = struct.pack(DATAGRAM_FORMAT, registerAddress | 128, value & 4294967295)
        self._TMC4330__connection.send_datagram(datagram, DATAGRAM_LENGTH, self._TMC4330__channel)

    def readRegister(self, registerAddress, signed=False):
        datagram = struct.pack(DATAGRAM_FORMAT, registerAddress, 0)
        reply = self._TMC4330__connection.send_datagram(datagram, DATAGRAM_LENGTH, self._TMC4330__channel)
        values = struct.unpack(DATAGRAM_FORMAT, reply)
        value = values[1]
        if signed:
            return TMC_helpers.toSigned32(value)
        return value

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0]), field[1], field[2], value))

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0]), field[1], field[2])

    def moveBy(self, motor, distance, velocity):
        if not 0 <= motor < self.MOTORS:
            raise ValueError
        position = self.readRegister((self.registers.XACTUAL), signed=True)
        self.moveTo(motor, position + distance, velocity)
        return position + distance

    def get_pin_state(self):
        pass