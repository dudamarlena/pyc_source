# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\protocols\layer4\udp.py
# Compiled at: 2010-05-01 15:45:14
"""
User Datagram Protocol (TCP/IP protocol stack)
"""
from construct import *
udp_header = Struct('udp_header', Value('header_length', lambda ctx: 8), UBInt16('source'), UBInt16('destination'), ExprAdapter(UBInt16('payload_length'), encoder=lambda obj, ctx: obj + 8, decoder=lambda obj, ctx: obj - 8), UBInt16('checksum'))
if __name__ == '__main__':
    cap = ('0bcc003500280689').decode('hex')
    obj = udp_header.parse(cap)
    print obj
    print repr(udp_header.build(obj))