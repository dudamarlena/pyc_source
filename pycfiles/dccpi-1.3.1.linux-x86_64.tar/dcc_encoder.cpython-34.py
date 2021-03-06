# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/dccpi/dcc_encoder.py
# Compiled at: 2016-11-05 00:32:57
# Size of source mod 2**32: 3030 bytes
"""
    Copyright (C) 2016  Hector Sanjuan

    This file is part of "dccpi".

    "dccpi" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "dccpi" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "dccpi".  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
from .dcc_packet_factory import DCCPacketFactory

class DCCEncoder(object):
    __doc__ = '\n    A DCC encoder takes a packet or packets and encodes them into the\n    DCC protocol electrical standard.\n\n    This class is meant to be extended by subclasses that implement\n    the relevant methods to actually send the bits (a dummy output would only\n    print it in screen, a RPI class would use GPIO to send them)\n    '
    MICROSECOND_DIV = 1000000.0

    def __init__(self, bit_one_part_min_duration=55, bit_one_part_max_duration=61, bit_one_part_duration=58, bit_zero_part_min_duration=95, bit_zero_part_max_duration=9900, bit_zero_part_duration=100, packet_separation=0):
        self.bit_one_part_min_duration = bit_one_part_min_duration
        self.bit_one_part_max_duration = bit_one_part_max_duration
        self.bit_one_part_duration = bit_one_part_duration
        self.bit_zero_part_min_duration = bit_zero_part_min_duration
        self.bit_zero_part_max_duration = bit_zero_part_max_duration
        self.bit_zero_part_duration = bit_zero_part_duration
        self.packet_separation = packet_separation
        self._payload = []
        self.idle_packet = DCCPacketFactory.idle_packet()
        self.reset_packet = DCCPacketFactory.reset_packet()
        self.stop_packet = DCCPacketFactory.stop_packet()

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, p):
        self._payload = p

    def send_idle(self, times):
        self.send_packet(self.idle_packet, times)

    def send_stop(self, times):
        self.send_packet(self.stop_packet, times)

    def send_reset(self, times):
        self.send_packet(self.reset_packet, times)

    def send_packet(self, packet, times):
        sys.stderr.write('send_packet() not implemented!')
        return False

    def send_payload(self, times):
        sys.stderr.write('send_payload() not implemented!')
        return False

    def tracks_power_on(self):
        print('Tracks powered ON')

    def tracks_power_off(self):
        print('Tracks powered OFF')