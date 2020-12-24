# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/dccpi/dcc_dummy_encoder.py
# Compiled at: 2016-11-05 00:32:57
# Size of source mod 2**32: 1566 bytes
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
from .dcc_encoder import DCCEncoder
import time

class DCCDummyEncoder(DCCEncoder):
    __doc__ = '\n    This class is meant to easy test that the controller\n    is correctly sending packages as it should and print\n    the packages to screen... nothing else. It sleeps\n    10 secs between packets batch\n    '
    SLEEP_BETWEEN_BATCHES = 10

    def __init__(self):
        DCCEncoder.__init__(self)

    def send_packet(self, packet, times):
        print(packet)
        print('(%d times...)' % times)
        time.sleep(self.SLEEP_BETWEEN_BATCHES)
        return True

    def send_payload(self, times):
        if not len(self.payload):
            return False
        print('----')
        for p in self.payload:
            print(p)

        print('---- (%d times...)' % times)
        time.sleep(self.SLEEP_BETWEEN_BATCHES)
        return True