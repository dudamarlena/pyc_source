# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/dccpi/dcc_packet_factory.py
# Compiled at: 2016-11-05 00:32:57
# Size of source mod 2**32: 5504 bytes
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
from bitstring import BitArray
from .dcc_general_packet import DCCGeneralPacket

class DCCPacketFactory:
    __doc__ = '\n    Make it easy to build packages types\n    '

    @staticmethod
    def speed_and_direction_packet(address, speed, speed_steps, direction, headlight=False):
        """
        Build a speed and direction packet.

        param address int is the dcc device address.
        param speed   int is the speed. Depending on the
                      speed steps we make a baseline packet
                      or a 128-bit packet
        param direction int is 1 for forward and 0 for backwards.
        """
        address_bin = BitArray('uint:8=%d' % address)
        if speed_steps == 128:
            instruction_bin1 = BitArray('0b00111111')
            instruction_bin2 = BitArray()
            if direction:
                instruction_bin2.append('0b1')
            else:
                instruction_bin2.append('0b0')
            speed_bin = BitArray('uint:7=%d' % speed)
            instruction_bin2.append(speed_bin)
            error = address_bin ^ instruction_bin1 ^ instruction_bin2
            data = [instruction_bin1, instruction_bin2, error]
        else:
            instruction_bin = BitArray('0b01')
            if direction:
                instruction_bin.append('0b1')
            else:
                instruction_bin.append('0b0')
            if speed_steps == 14:
                if headlight:
                    instruction_bin.append('0b1')
                else:
                    instruction_bin.append('0b0')
                speed_bin = BitArray('uint:4=%d' % speed)
            else:
                speed_bin = BitArray('uint:5=%d' % speed)
                speed_bin.ror(1)
            instruction_bin.append(speed_bin)
            error = address_bin ^ instruction_bin
            data = [instruction_bin, error]
        return DCCGeneralPacket(address_bin, data)

    @staticmethod
    def function_group_one_packet(address, fl, fl1, fl2, fl3, fl4):
        address_bin = BitArray('uint:8=%d' % address)
        functions = [
         fl, fl4, fl3, fl2, fl1]
        instruction_bin = BitArray('0b100')
        for f in functions:
            if f:
                instruction_bin.append('0b1')
            else:
                instruction_bin.append('0b0')

        error = address_bin ^ instruction_bin
        data = [instruction_bin, error]
        return DCCGeneralPacket(address_bin, data)

    @staticmethod
    def reset_packet():
        """
        Build a reset package for all decoders.

        All decoders shall erase all volatile memory, return
        to power-up state and bring locomotives to an immediate
        stop.
        """
        byte_one = BitArray('0b00000000')
        byte_two = BitArray('0b00000000')
        byte_three = BitArray('0b00000000')
        return DCCGeneralPacket(byte_one, [byte_two, byte_three])

    @staticmethod
    def idle_packet():
        """
        Build an idle packet for all decoders.

        Upon receiving, all decoders shall perform no new action and act
        like if it was a packet addressed to some other decoder.
        """
        byte_one = BitArray('0b11111111')
        byte_two = BitArray('0b00000000')
        byte_three = BitArray('0b11111111')
        return DCCGeneralPacket(byte_one, [byte_two, byte_three])

    @staticmethod
    def stop_packet(direction=1, soft_stop=False, ignore_direction=True):
        """
        Build a stop packet for all decoders.

        param direction sets the direction bit in the packet.
        param soft_stop indicates if the decoder bring the locomotive to stop
                        or stop delivering energy to the engine (guess in
                        the first case it may gradually decelerate it)
        param ignore_direction allows optionally ignoring the direction bit
                               for all direction sensitive functions
        """
        byte_one = BitArray('0b00000000')
        byte_two = BitArray('0b01')
        if direction:
            byte_two.append('0b1')
        else:
            byte_two.append('0b0')
        if ignore_direction:
            byte_two.append('0b1')
        else:
            byte_two.append('0b0')
        byte_two.append('0b000')
        if soft_stop:
            byte_two.append('0b0')
        else:
            byte_two.append('0b1')
        byte_three = byte_two.copy()
        return DCCGeneralPacket(byte_one, [byte_two, byte_three])