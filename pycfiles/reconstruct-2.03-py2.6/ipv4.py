# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\protocols\layer3\ipv4.py
# Compiled at: 2010-05-01 15:45:14
"""
Internet Protocol version 4 (TCP/IP protocol stack)
"""
from construct import *

class IpAddressAdapter(Adapter):

    def _encode(self, obj, context):
        return ('').join(chr(int(b)) for b in obj.split('.'))

    def _decode(self, obj, context):
        return ('.').join(str(ord(b)) for b in obj)


def IpAddress(name):
    return IpAddressAdapter(Bytes(name, 4))


def ProtocolEnum(code):
    return Enum(code, ICMP=1, TCP=6, UDP=17)


ipv4_header = Struct('ip_header', EmbeddedBitStruct(Const(Nibble('version'), 4), ExprAdapter(Nibble('header_length'), decoder=lambda obj, ctx: obj * 4, encoder=lambda obj, ctx: obj / 4)), BitStruct('tos', Bits('precedence', 3), Flag('minimize_delay'), Flag('high_throuput'), Flag('high_reliability'), Flag('minimize_cost'), Padding(1)), UBInt16('total_length'), Value('payload_length', lambda ctx: ctx.total_length - ctx.header_length), UBInt16('identification'), EmbeddedBitStruct(Struct('flags', Padding(1), Flag('dont_fragment'), Flag('more_fragments')), Bits('frame_offset', 13)), UBInt8('ttl'), ProtocolEnum(UBInt8('protocol')), UBInt16('checksum'), IpAddress('source'), IpAddress('destination'), Field('options', lambda ctx: ctx.header_length - 20))
if __name__ == '__main__':
    cap = ('4500003ca0e3000080116185c0a80205d474a126').decode('hex')
    obj = ipv4_header.parse(cap)
    print obj
    print repr(ipv4_header.build(obj))