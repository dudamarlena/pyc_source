# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/awaldron/Projects/ait/ait-gui/ait/gui/bin/ait_example.py
# Compiled at: 2018-11-28 19:09:32
import socket, struct, time
from ait.core import tlm
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hs_packet = struct.Struct('>hhhhh')
for i in range(100):
    buf = hs_packet.pack(i, i, i, i, i)
    s.sendto(buf, ('localhost', 3076))
    time.sleep(1)