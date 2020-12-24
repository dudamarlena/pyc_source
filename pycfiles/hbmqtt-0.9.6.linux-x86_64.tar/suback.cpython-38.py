# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/suback.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 2488 bytes
import asyncio
from hbmqtt.mqtt.packet import MQTTPacket, MQTTFixedHeader, SUBACK, PacketIdVariableHeader, MQTTPayload, MQTTVariableHeader
from hbmqtt.errors import HBMQTTException, NoDataException
from hbmqtt.adapters import ReaderAdapter
from hbmqtt.codecs import bytes_to_int, int_to_bytes, read_or_raise

class SubackPayload(MQTTPayload):
    __slots__ = ('return_codes', )
    RETURN_CODE_00 = 0
    RETURN_CODE_01 = 1
    RETURN_CODE_02 = 2
    RETURN_CODE_80 = 128

    def __init__(self, return_codes=[]):
        super().__init__()
        self.return_codes = return_codes

    def __repr__(self):
        return type(self).__name__ + '(return_codes={0})'.format(repr(self.return_codes))

    def to_bytes(self, fixed_header: MQTTFixedHeader, variable_header: MQTTVariableHeader):
        out = b''
        for return_code in self.return_codes:
            out += int_to_bytes(return_code, 1)
        else:
            return out

    @classmethod
    @asyncio.coroutine
    def from_stream(cls, reader: ReaderAdapter, fixed_header: MQTTFixedHeader, variable_header: MQTTVariableHeader):
        return_codes = []
        bytes_to_read = fixed_header.remaining_length - variable_header.bytes_length
        for i in range(0, bytes_to_read):
            try:
                return_code_byte = yield from read_or_raise(reader, 1)
                return_code = bytes_to_int(return_code_byte)
                return_codes.append(return_code)
            except NoDataException:
                break

        else:
            return cls(return_codes)

        if False:
            yield None


class SubackPacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = SubackPayload

    def __init__(self, fixed=None, variable_header=None, payload=None):
        if fixed is None:
            header = MQTTFixedHeader(SUBACK, 0)
        else:
            if fixed.packet_type is not SUBACK:
                raise HBMQTTException('Invalid fixed packet type %s for SubackPacket init' % fixed.packet_type)
            header = fixed
        super().__init__(header)
        self.variable_header = variable_header
        self.payload = payload

    @classmethod
    def build(cls, packet_id, return_codes):
        variable_header = cls.VARIABLE_HEADER(packet_id)
        payload = cls.PAYLOAD(return_codes)
        return cls(variable_header=variable_header, payload=payload)