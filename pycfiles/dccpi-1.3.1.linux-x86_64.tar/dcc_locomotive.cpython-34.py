# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/dccpi/dcc_locomotive.py
# Compiled at: 2016-11-05 00:32:57
# Size of source mod 2**32: 5715 bytes
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
from .dcc_packet_factory import DCCPacketFactory
import sys

class DCCLocomotive(object):
    __doc__ = '\n    A locomotive can be understood as a decoder that\n    is able to understand speed and direction packets,\n    as well as function group one packets (for the moment)\n    '

    def __init__(self, name, address, speed=0, speed_steps=28, direction=1, fl=False, f1=False, f2=False, f3=False, f4=False):
        self.notify_update_callback = None
        self.name = name
        self._address = address
        self.direction = direction
        self._speed = 0
        self.fl = fl
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.f4 = f4
        self.speed_steps = speed_steps
        self.speed = speed

    def __str__(self):
        str = '\nDCC locomotive\nName:               %s\nAddress:            %i\nSpeed:              %i\nSpeed steps:        %i\nDirection:          %i\nFL, F1, F2, F3, F4: [%i %i %i %i %i]\n'
        return str % (self.name, self.address, self.speed, self.speed_steps,
         self.direction, self.fl, self.f1, self.f2,
         self.f3, self.f4)

    def __repr__(self):
        return self.__str__()

    def emergency_stop(self):
        self.speed = 1

    def stop(self):
        self.speed = 0

    def reverse(self):
        self.direction = 0 if self.direction else 1
        self._notify_update()

    @property
    def speed_steps(self):
        return self._speed_steps

    @speed_steps.setter
    def speed_steps(self, ss):
        if int(ss) in (14, 28, 128):
            self._speed_steps = int(ss)
        else:
            m = 'Speed steps must be 14, 28 or 128. We have set it to 28\n'
            sys.stderr.write(m)
            self._speed_steps = 28
        self.speed = self.speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        speed = abs(speed)
        if self.speed_steps == 14:
            self._speed = min(15, speed)
        else:
            if self.speed_steps == 28:
                self._speed = min(31, speed)
            elif self.speed_steps == 128:
                self._speed = min(127, speed)
        self._notify_update()

    @property
    def fl(self):
        return self._fl

    @fl.setter
    def fl(self, x):
        if x:
            self._fl = True
        else:
            self._fl = False
        self._notify_update()

    @property
    def f1(self):
        return self._f1

    @f1.setter
    def f1(self, x):
        if x:
            self._f1 = True
        else:
            self._f1 = False
        self._notify_update()

    @property
    def f2(self):
        return self._f2

    @f2.setter
    def f2(self, x):
        if x:
            self._f2 = True
        else:
            self._f2 = False
        self._notify_update()

    @property
    def f3(self):
        return self._f3

    @f3.setter
    def f3(self, x):
        if x:
            self._f3 = True
        else:
            self._f3 = False
        self._notify_update()

    @property
    def f4(self):
        return self._f4

    @f4.setter
    def f4(self, x):
        if x:
            self._f4 = True
        else:
            self._f4 = False
        self._notify_update()

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, ad):
        self._address = ad
        self._notify_update()

    def switch_headlight(self):
        self.fl = False if self.fl else True

    def slower(self):
        if self.speed is 2:
            self.speed = 0
        else:
            self.speed = self.speed - 1

    def faster(self):
        if self.speed is 0:
            self.speed = 2
        else:
            self.speed = self.speed + 1

    def control_packets(self):
        factory = DCCPacketFactory
        speed_packet = factory.speed_and_direction_packet(self.address, self.speed, self.speed_steps, self.direction, self.fl)
        function_group_one_packet = factory.function_group_one_packet(self.address, self.fl, self.f1, self.f2, self.f3, self.f4)
        return [
         speed_packet, function_group_one_packet]

    def _notify_update(self):
        """
        Used by the DCC controller to generate a new set
        of packets with updated information for the encoder
        """
        if self.notify_update_callback:
            self.notify_update_callback(self.name)