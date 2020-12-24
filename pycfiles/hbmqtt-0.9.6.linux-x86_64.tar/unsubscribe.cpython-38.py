# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/unsubscribe.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 2212 bytes
import asyncio
from hbmqtt.mqtt.packet import MQTTPacket, MQTTFixedHeader, UNSUBSCRIBE, PacketIdVariableHeader, MQTTPayload, MQTTVariableHeader
from hbmqtt.errors import HBMQTTException, NoDataException
from hbmqtt.codecs import decode_string, encode_string

class UnubscribePayload(MQTTPayload):
    __slots__ = ('topics', )

    def __init__(self, topics=[]):
        super().__init__()
        self.topics = topics

    def to_bytes(self, fixed_header: MQTTFixedHeader, variable_header: MQTTVariableHeader):
        out = b''
        for topic in self.topics:
            out += encode_string(topic)
        else:
            return out

    @classmethod
    @asyncio.coroutine
    def from_stream--- This code section failed: ---

 L.  29         0  BUILD_LIST_0          0 
                2  STORE_FAST               'topics'

 L.  30         4  LOAD_FAST                'fixed_header'
                6  LOAD_ATTR                remaining_length
                8  LOAD_FAST                'variable_header'
               10  LOAD_ATTR                bytes_length
               12  BINARY_SUBTRACT  
               14  STORE_FAST               'payload_length'

 L.  31        16  LOAD_CONST               0
               18  STORE_FAST               'read_bytes'

 L.  32        20  LOAD_FAST                'read_bytes'
               22  LOAD_FAST                'payload_length'
               24  COMPARE_OP               <
               26  POP_JUMP_IF_FALSE   106  'to 106'

 L.  33        28  SETUP_FINALLY        80  'to 80'

 L.  34        30  LOAD_GLOBAL              decode_string
               32  LOAD_FAST                'reader'
               34  CALL_FUNCTION_1       1  ''
               36  GET_YIELD_FROM_ITER
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  STORE_FAST               'topic'

 L.  35        44  LOAD_FAST                'topics'
               46  LOAD_METHOD              append
               48  LOAD_FAST                'topic'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L.  36        54  LOAD_FAST                'read_bytes'
               56  LOAD_CONST               2
               58  LOAD_GLOBAL              len
               60  LOAD_FAST                'topic'
               62  LOAD_METHOD              encode
               64  LOAD_STR                 'utf-8'
               66  CALL_METHOD_1         1  ''
               68  CALL_FUNCTION_1       1  ''
               70  BINARY_ADD       
               72  INPLACE_ADD      
               74  STORE_FAST               'read_bytes'
               76  POP_BLOCK        
               78  JUMP_BACK            20  'to 20'
             80_0  COME_FROM_FINALLY    28  '28'

 L.  37        80  DUP_TOP          
               82  LOAD_GLOBAL              NoDataException
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   102  'to 102'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L.  38        94  POP_EXCEPT       
               96  BREAK_LOOP          106  'to 106'
               98  POP_EXCEPT       
              100  JUMP_BACK            20  'to 20'
            102_0  COME_FROM            86  '86'
              102  END_FINALLY      
              104  JUMP_BACK            20  'to 20'
            106_0  COME_FROM_EXCEPT_CLAUSE    96  '96'
            106_1  COME_FROM_EXCEPT_CLAUSE    26  '26'

 L.  39       106  LOAD_FAST                'cls'
              108  LOAD_FAST                'topics'
              110  CALL_FUNCTION_1       1  ''
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 106_1


class UnsubscribePacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = UnubscribePayload

    def __init__(self, fixed=None, variable_header=None, payload=None):
        if fixed is None:
            header = MQTTFixedHeader(UNSUBSCRIBE, 2)
        else:
            if fixed.packet_type is not UNSUBSCRIBE:
                raise HBMQTTException('Invalid fixed packet type %s for UnsubscribePacket init' % fixed.packet_type)
            header = fixed
        super().__init__header
        self.variable_header = variable_header
        self.payload = payload

    @classmethod
    def build(cls, topics, packet_id):
        v_header = PacketIdVariableHeader(packet_id)
        payload = UnubscribePayload(topics)
        return UnsubscribePacket(variable_header=v_header, payload=payload)