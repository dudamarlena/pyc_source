# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC6200\TMC6200.py
# Compiled at: 2020-01-31 04:12:12
# Size of source mod 2**32: 2048 bytes
"""
Created on 06.03.2019

@author: ED
"""
import struct
import PyTrinamic.ic.TMC6200.TMC6200_register as TMC6200_register
import PyTrinamic.ic.TMC6200.TMC6200_register_variant as TMC6200_register_variant
import PyTrinamic.ic.TMC6200.TMC6200_fields as TMC6200_fields
from PyTrinamic.helpers import TMC_helpers
DATAGRAM_FORMAT = '>BI'
DATAGRAM_LENGTH = 5

class TMC6200:
    __doc__ = '\n    Class for the TMC6200 IC\n    '

    def __init__(self, connection, channel=0):
        self._TMC6200__connection = connection
        self._TMC6200__channel = channel
        self.registers = TMC6200_register
        self.fields = TMC6200_fields
        self.variants = TMC6200_register_variant
        self.MOTORS = 1

    def showChipInfo(self):
        print('TMC6200 chip info: The TMC6200 is a high-power gate-driver for PMSM servo or BLDC motors. Voltage supply: 8 - 60V')

    def writeRegister(self, registerAddress, value, channel=None):
        del channel
        datagram = struct.pack(DATAGRAM_FORMAT, registerAddress | 128, value)
        self._TMC6200__connection.send_datagram(datagram, DATAGRAM_LENGTH)

    def readRegister(self, registerAddress, signed=False, channel=None):
        del channel
        datagram = struct.pack(DATAGRAM_FORMAT, registerAddress, 0)
        reply = self._TMC6200__connection.send_datagram(datagram, DATAGRAM_LENGTH)
        values = struct.unpack(DATAGRAM_FORMAT, reply)
        value = values[1]
        if signed:
            return TMC_helpers.toSigned32(value)
        return value

    def writeRegisterField(self, field, value):
        return self.writeRegister(field[0], TMC_helpers.field_set(self.readRegister(field[0], self._TMC6200__channel), field[1], field[2], value), self._TMC6200__channel)

    def readRegisterField(self, field):
        return TMC_helpers.field_get(self.readRegister(field[0], self._TMC6200__channel), field[1], field[2])

    def get_pin_state(self):
        pass