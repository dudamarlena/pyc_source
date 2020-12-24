# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\protocols\layer2\ethernet.py
# Compiled at: 2010-05-01 15:45:14
"""
Ethernet (TCP/IP protocol stack)
"""
from construct import *

class MacAddressAdapter(Adapter):

    def _encode(self, obj, context):
        return obj.replace('-', '').decode('hex')

    def _decode(self, obj, context):
        return ('-').join(b.encode('hex') for b in obj)


def MacAddress(name):
    return MacAddressAdapter(Bytes(name, 6))


ethernet_header = Struct('ethernet_header', MacAddress('destination'), MacAddress('source'), Enum(UBInt16('type'), IPv4=2048, ARP=2054, RARP=32821, X25=2053, IPX=33079, IPv6=34525, _default_=Pass))
if __name__ == '__main__':
    cap = ('0011508c283c0002e34260090800').decode('hex')
    obj = ethernet_header.parse(cap)
    print obj
    print repr(ethernet_header.build(obj))