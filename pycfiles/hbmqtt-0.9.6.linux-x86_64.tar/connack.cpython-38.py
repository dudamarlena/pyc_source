# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/connack.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 2776 bytes
import asyncio
from hbmqtt.mqtt.packet import CONNACK, MQTTPacket, MQTTFixedHeader, MQTTVariableHeader
from hbmqtt.codecs import read_or_raise, bytes_to_int
from hbmqtt.errors import HBMQTTException
from hbmqtt.adapters import ReaderAdapter
CONNECTION_ACCEPTED = 0
UNACCEPTABLE_PROTOCOL_VERSION = 1
IDENTIFIER_REJECTED = 2
SERVER_UNAVAILABLE = 3
BAD_USERNAME_PASSWORD = 4
NOT_AUTHORIZED = 5

class ConnackVariableHeader(MQTTVariableHeader):
    __slots__ = ('session_parent', 'return_code')

    def __init__(self, session_parent=None, return_code=None):
        super().__init__()
        self.session_parent = session_parent
        self.return_code = return_code

    @classmethod
    @asyncio.coroutine
    def from_stream(cls, reader: ReaderAdapter, fixed_header: MQTTFixedHeader):
        data = yield from read_or_raise(reader, 2)
        session_parent = data[0] & 1
        return_code = bytes_to_int(data[1])
        return cls(session_parent, return_code)
        if False:
            yield None

    def to_bytes(self):
        out = bytearray(2)
        if self.session_parent:
            out[0] = 1
        else:
            out[0] = 0
        out[1] = self.return_code
        return out

    def __repr__(self):
        return type(self).__name__ + '(session_parent={0}, return_code={1})'.format(hex(self.session_parent), hex(self.return_code))


class ConnackPacket(MQTTPacket):
    VARIABLE_HEADER = ConnackVariableHeader
    PAYLOAD = None

    @property
    def return_code(self):
        return self.variable_header.return_code

    @return_code.setter
    def return_code(self, return_code):
        self.variable_header.return_code = return_code

    @property
    def session_parent(self):
        return self.variable_header.session_parent

    @session_parent.setter
    def session_parent(self, session_parent):
        self.variable_header.session_parent = session_parent

    def __init__(self, fixed=None, variable_header=None, payload=None):
        if fixed is None:
            header = MQTTFixedHeader(CONNACK, 0)
        else:
            if fixed.packet_type is not CONNACK:
                raise HBMQTTException('Invalid fixed packet type %s for ConnackPacket init' % fixed.packet_type)
            header = fixed
        super().__init__(header)
        self.variable_header = variable_header
        self.payload = None

    @classmethod
    def build(cls, session_parent=None, return_code=None):
        v_header = ConnackVariableHeader(session_parent, return_code)
        packet = ConnackPacket(variable_header=v_header)
        return packet