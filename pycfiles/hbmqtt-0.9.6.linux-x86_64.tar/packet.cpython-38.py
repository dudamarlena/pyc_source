# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/packet.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 7687 bytes
import asyncio
from hbmqtt.codecs import bytes_to_hex_str, decode_packet_id, int_to_bytes, read_or_raise
from hbmqtt.errors import CodecException, MQTTException, NoDataException
from hbmqtt.adapters import ReaderAdapter, WriterAdapter
from datetime import datetime
from struct import unpack
RESERVED_0 = 0
CONNECT = 1
CONNACK = 2
PUBLISH = 3
PUBACK = 4
PUBREC = 5
PUBREL = 6
PUBCOMP = 7
SUBSCRIBE = 8
SUBACK = 9
UNSUBSCRIBE = 10
UNSUBACK = 11
PINGREQ = 12
PINGRESP = 13
DISCONNECT = 14
RESERVED_15 = 15

class MQTTFixedHeader:
    __slots__ = ('packet_type', 'remaining_length', 'flags')

    def __init__(self, packet_type, flags=0, length=0):
        self.packet_type = packet_type
        self.remaining_length = length
        self.flags = flags

    def to_bytes(self):

        def encode_remaining_length(length: int):
            encoded = bytearray()
            while True:
                length_byte = length % 128
                length //= 128
                if length > 0:
                    length_byte |= 128
                encoded.append(length_byte)
                if length <= 0:
                    break

            return encoded

        out = bytearray()
        packet_type = 0
        try:
            packet_type = self.packet_type << 4 | self.flags
            out.append(packet_type)
        except OverflowError:
            raise CodecException('packet_type encoding exceed 1 byte length: value=%d', packet_type)
        else:
            encoded_length = encode_remaining_length(self.remaining_length)
            out.extend(encoded_length)
            return out

    @asyncio.coroutine
    def to_stream(self, writer: WriterAdapter):
        writer.write(self.to_bytes())

    @property
    def bytes_length(self):
        return len(self.to_bytes())

    @classmethod
    @asyncio.coroutine
    def from_stream--- This code section failed: ---

 L.  81         0  LOAD_GLOBAL              asyncio
                2  LOAD_ATTR                coroutine

 L.  82         4  LOAD_CLOSURE             'msg_type'
                6  LOAD_CLOSURE             'reader'
                8  BUILD_TUPLE_2         2 
               10  LOAD_CODE                <code_object decode_remaining_length>
               12  LOAD_STR                 'MQTTFixedHeader.from_stream.<locals>.decode_remaining_length'
               14  MAKE_FUNCTION_8          'closure'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'decode_remaining_length'

 L. 103        20  SETUP_FINALLY       102  'to 102'

 L. 104        22  LOAD_GLOBAL              read_or_raise
               24  LOAD_DEREF               'reader'
               26  LOAD_CONST               1
               28  CALL_FUNCTION_2       2  ''
               30  GET_YIELD_FROM_ITER
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  STORE_FAST               'byte1'

 L. 105        38  LOAD_GLOBAL              unpack
               40  LOAD_STR                 '!B'
               42  LOAD_FAST                'byte1'
               44  CALL_FUNCTION_2       2  ''
               46  STORE_FAST               'int1'

 L. 106        48  LOAD_FAST                'int1'
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  LOAD_CONST               240
               56  BINARY_AND       
               58  LOAD_CONST               4
               60  BINARY_RSHIFT    
               62  STORE_DEREF              'msg_type'

 L. 107        64  LOAD_FAST                'int1'
               66  LOAD_CONST               0
               68  BINARY_SUBSCR    
               70  LOAD_CONST               15
               72  BINARY_AND       
               74  STORE_FAST               'flags'

 L. 108        76  LOAD_FAST                'decode_remaining_length'
               78  CALL_FUNCTION_0       0  ''
               80  GET_YIELD_FROM_ITER
               82  LOAD_CONST               None
               84  YIELD_FROM       
               86  STORE_FAST               'remain_length'

 L. 110        88  LOAD_FAST                'cls'
               90  LOAD_DEREF               'msg_type'
               92  LOAD_FAST                'flags'
               94  LOAD_FAST                'remain_length'
               96  CALL_FUNCTION_3       3  ''
               98  POP_BLOCK        
              100  RETURN_VALUE     
            102_0  COME_FROM_FINALLY    20  '20'

 L. 111       102  DUP_TOP          
              104  LOAD_GLOBAL              NoDataException
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   122  'to 122'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 112       116  POP_EXCEPT       
              118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM           108  '108'
              122  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 112

    def __repr__(self):
        return type(self).__name__ + '(length={0}, flags={1})'.format(self.remaining_length, hex(self.flags))


class MQTTVariableHeader:

    def __init__(self):
        pass

    @asyncio.coroutine
    def to_stream(self, writer: asyncio.StreamWriter):
        writer.write(self.to_bytes())
        (yield from writer.drain())
        if False:
            yield None

    def to_bytes(self) -> bytes:
        """
        Serialize header data to a byte array conforming to MQTT protocol
        :return: serialized data
        """
        pass

    @property
    def bytes_length(self):
        return len(self.to_bytes())

    @classmethod
    @asyncio.coroutine
    def from_stream(cls, reader: asyncio.StreamReader, fixed_header: MQTTFixedHeader):
        pass


class PacketIdVariableHeader(MQTTVariableHeader):
    __slots__ = ('packet_id', )

    def __init__(self, packet_id):
        super().__init__()
        self.packet_id = packet_id

    def to_bytes(self):
        out = b''
        out += int_to_bytes(self.packet_id, 2)
        return out

    @classmethod
    @asyncio.coroutine
    def from_stream(cls, reader: ReaderAdapter, fixed_header: MQTTFixedHeader):
        packet_id = yield from decode_packet_id(reader)
        return cls(packet_id)
        if False:
            yield None

    def __repr__(self):
        return type(self).__name__ + '(packet_id={0})'.format(self.packet_id)


class MQTTPayload:

    def __init__(self):
        pass

    @asyncio.coroutine
    def to_stream(self, writer: asyncio.StreamWriter):
        writer.write(self.to_bytes())
        (yield from writer.drain())
        if False:
            yield None

    def to_bytes(self, fixed_header: MQTTFixedHeader, variable_header: MQTTVariableHeader):
        pass

    @classmethod
    @asyncio.coroutine
    def from_stream(cls, reader: asyncio.StreamReader, fixed_header: MQTTFixedHeader, variable_header: MQTTVariableHeader):
        pass


class MQTTPacket:
    __slots__ = ('fixed_header', 'variable_header', 'payload', 'protocol_ts')
    FIXED_HEADER = MQTTFixedHeader
    VARIABLE_HEADER = None
    PAYLOAD = None

    def __init__(self, fixed: MQTTFixedHeader, variable_header: MQTTVariableHeader=None, payload: MQTTPayload=None):
        self.fixed_header = fixed
        self.variable_header = variable_header
        self.payload = payload
        self.protocol_ts = None

    @asyncio.coroutine
    def to_stream(self, writer: asyncio.StreamWriter):
        writer.write(self.to_bytes())
        (yield from writer.drain())
        self.protocol_ts = datetime.now()
        if False:
            yield None

    def to_bytes(self) -> bytes:
        if self.variable_header:
            variable_header_bytes = self.variable_header.to_bytes()
        else:
            variable_header_bytes = b''
        if self.payload:
            payload_bytes = self.payload.to_bytes(self.fixed_header, self.variable_header)
        else:
            payload_bytes = b''
        self.fixed_header.remaining_length = len(variable_header_bytes) + len(payload_bytes)
        fixed_header_bytes = self.fixed_header.to_bytes()
        return fixed_header_bytes + variable_header_bytes + payload_bytes

    @classmethod
    @asyncio.coroutine
    def from_stream(cls, reader: ReaderAdapter, fixed_header=None, variable_header=None):
        if fixed_header is None:
            fixed_header = yield from cls.FIXED_HEADER.from_stream(reader)
        else:
            if cls.VARIABLE_HEADER:
                if variable_header is None:
                    variable_header = yield from cls.VARIABLE_HEADER.from_stream(reader, fixed_header)
                else:
                    variable_header = None
            elif cls.PAYLOAD:
                payload = yield from cls.PAYLOAD.from_stream(reader, fixed_header, variable_header)
            else:
                payload = None
            if fixed_header:
                instance = variable_header or payload or cls(fixed_header)
            else:
                pass
            if fixed_header:
                instance = payload or cls(fixed_header, variable_header)
            else:
                instance = cls(fixed_header, variable_header, payload)
        instance.protocol_ts = datetime.now()
        return instance
        if False:
            yield None

    @property
    def bytes_length(self):
        return len(self.to_bytes())

    def __repr__(self):
        return type(self).__name__ + '(ts={0!s}, fixed={1!r}, variable={2!r}, payload={3!r})'.format(self.protocol_ts, self.fixed_header, self.variable_header, self.payload)