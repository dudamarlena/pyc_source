# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC4671\TMC4671.py
# Compiled at: 2019-11-27 05:44:23
# Size of source mod 2**32: 2267 bytes
"""
Created on 02.01.2019

@author: ED
"""
import struct
import PyTrinamic.ic.TMC4671.TMC4671_register as TMC4671_register
import PyTrinamic.ic.TMC4671.TMC4671_register_variant as TMC4671_register_variant
import PyTrinamic.ic.TMC4671.TMC4671_fields as TMC4671_fields
from PyTrinamic.helpers import TMC_helpers
DATAGRAM_FORMAT = '>BI'
DATAGRAM_LENGTH = 5

class TMC4671:
    __doc__ = '\n    Class for the TMC4671 IC\n    '

    def __init__(self, connection, channel=0):
        self._TMC4671__connection = connection
        self._TMC4671__channel = channel
        self.registers = TMC4671_register
        self.fields = TMC4671_fields
        self.variants = TMC4671_register_variant
        self.MOTORS = 1

    def showChipInfo(self):
        print('TMC4671 chip info: The TMC4671 is a fully integreated servo controller, providing Field Orianted Control for BLDC/PMSM and 2-phase Stepper Motors as well as DC motors and voice coils. Voltage supply: 0 - 80V')

    def writeRegister(self, registerAddress, value):
        datagram = struct.pack(DATAGRAM_FORMAT, registerAddress | 128, value & 4294967295)
        self._TMC4671__connection.send_datagram(datagram, DATAGRAM_LENGTH, self._TMC4671__channel)

    def readRegister(self, registerAddress, signed=False):
        datagram = struct.pack(DATAGRAM_FORMAT, registerAddress, 0)
        reply = self._TMC4671__connection.send_datagram(datagram, DATAGRAM_LENGTH, self._TMC4671__channel)
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