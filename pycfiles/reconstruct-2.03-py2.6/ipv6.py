# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\protocols\layer3\ipv6.py
# Compiled at: 2010-05-01 15:45:14
"""
Internet Protocol version 6 (TCP/IP protocol stack)
"""
from construct import *
from ipv4 import ProtocolEnum

class Ipv6AddressAdapter(Adapter):

    def _encode(self, obj, context):
        return ('').join(part.decode('hex') for part in obj.split(':'))

    def _decode(self, obj, context):
        return (':').join(b.encode('hex') for b in obj)


def Ipv6Address(name):
    return Ipv6AddressAdapter(Bytes(name, 16))


ipv6_header = Struct('ip_header', EmbeddedBitStruct(OneOf(Bits('version', 4), [6]), Bits('traffic_class', 8), Bits('flow_label', 20)), UBInt16('payload_length'), ProtocolEnum(UBInt8('protocol')), UBInt8('hoplimit'), Alias('ttl', 'hoplimit'), Ipv6Address('source'), Ipv6Address('destination'))
if __name__ == '__main__':
    o = ipv6_header.parse(b'o\xf0\x00\x00\x01\x02\x06\x800123456789ABCDEFFEDCBA9876543210')
    print o
    print repr(ipv6_header.build(o))