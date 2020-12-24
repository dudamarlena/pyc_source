# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/txXBee/protocol.py
# Compiled at: 2012-02-23 17:23:09
"""
Copyright (C) 2011 Wagner Sartori Junior <wsartori@gmail.com>
http://www.wsartori.com

This file is part of txXBee.

txXBee program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from xbee.zigbee import ZigBee
from xbee.base import XBeeBase
from xbee.frame import APIFrame
from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

class txXBee(protocol.Protocol, ZigBee):

    def __init__(self, escaped=True):
        self._escaped = escaped
        self._frame = None
        return

    def dataReceived(self, data):
        for c in data:
            if self._frame:
                self._frame.fill(c)
                if self._frame.remaining_bytes() == 0:
                    try:
                        self._frame.parse()
                        self.handle_packet(self._split_response(self._frame.data))
                    except ValueError:
                        self.handle_badframe(self._frame.raw_data)

                    self._frame = None
            elif c == APIFrame.START_BYTE:
                self._frame = APIFrame(escaped=self._escaped)
                self._frame.fill(c)

        return

    def handle_packet(self, packet):
        pass

    def handle_badframe(self, packet):
        pass

    def _write(self, data):
        frame = APIFrame(data, self._escaped).output()
        self.transport.write(frame)