# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mjjoyce/Coding/AIT/GUI/AIT-GUI/ait/gui/bin/ait_example.py
# Compiled at: 2019-08-29 14:54:40
# Size of source mod 2**32: 275 bytes
import socket, struct, time
from ait.core import tlm
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hs_packet = struct.Struct('>hhhhh')
for i in range(100):
    buf = hs_packet.pack(i, i, i, i, i)
    s.sendto(buf, ('localhost', 3076))
    time.sleep(1)