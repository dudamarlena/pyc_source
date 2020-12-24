# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/subscribe.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 2512 bytes
import asyncio
from hbmqtt.mqtt.packet import MQTTPacket, MQTTFixedHeader, SUBSCRIBE, PacketIdVariableHeader, MQTTPayload, MQTTVariableHeader
from hbmqtt.errors import HBMQTTException, NoDataException
from hbmqtt.codecs import bytes_to_int, decode_string, encode_string, int_to_bytes, read_or_raise

class SubscribePayload(MQTTPayload):
    __slots__ = ('topics', )

    def __init__(self, topics=[]):
        super().__init__()
        self.topics = topics

    def to_bytes(self, fixed_header: MQTTFixedHeader, variable_header: MQTTVariableHeader):
        out = b''
        for topic in self.topics:
            out += encode_string(topic[0])
            out += int_to_bytes(topic[1], 1)
        else:
            return out

    @classmethod
    @asyncio.coroutine
    def from_stream--- This code section failed: ---

 L.  30         0  BUILD_LIST_0          0 
                2  STORE_FAST               'topics'

 L.  31         4  LOAD_FAST                'fixed_header'
                6  LOAD_ATTR                remaining_length
                8  LOAD_FAST                'variable_header'
               10  LOAD_ATTR                bytes_length
               12  BINARY_SUBTRACT  
               14  STORE_FAST               'payload_length'

 L.  32        16  LOAD_CONST               0
               18  STORE_FAST               'read_bytes'

 L.  33        20  LOAD_FAST                'read_bytes'
               22  LOAD_FAST                'payload_length'
               24  COMPARE_OP               <
               26  POP_JUMP_IF_FALSE   156  'to 156'

 L.  34        28  SETUP_FINALLY       112  'to 112'

 L.  35        30  LOAD_GLOBAL              decode_string
               32  LOAD_FAST                'reader'
               34  CALL_FUNCTION_1       1  ''
               36  GET_YIELD_FROM_ITER
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  STORE_FAST               'topic'

 L.  36        44  LOAD_GLOBAL              read_or_raise
               46  LOAD_FAST                'reader'
               48  LOAD_CONST               1
               50  CALL_FUNCTION_2       2  ''
               52  GET_YIELD_FROM_ITER
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  STORE_FAST               'qos_byte'

 L.  37        60  LOAD_GLOBAL              bytes_to_int
               62  LOAD_FAST                'qos_byte'
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'qos'

 L.  38        68  LOAD_FAST                'topics'
               70  LOAD_METHOD              append
               72  LOAD_FAST                'topic'
               74  LOAD_FAST                'qos'
               76  BUILD_TUPLE_2         2 
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L.  39        82  LOAD_FAST                'read_bytes'
               84  LOAD_CONST               2
               86  LOAD_GLOBAL              len
               88  LOAD_FAST                'topic'
               90  LOAD_METHOD              encode
               92  LOAD_STR                 'utf-8'
               94  CALL_METHOD_1         1  ''
               96  CALL_FUNCTION_1       1  ''
               98  BINARY_ADD       
              100  LOAD_CONST               1
              102  BINARY_ADD       
              104  INPLACE_ADD      
              106  STORE_FAST               'read_bytes'
              108  POP_BLOCK        
              110  JUMP_BACK            20  'to 20'
            112_0  COME_FROM_FINALLY    28  '28'

 L.  40       112  DUP_TOP          
              114  LOAD_GLOBAL              NoDataException
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   152  'to 152'
              120  POP_TOP          
              122  STORE_FAST               'exc'
              124  POP_TOP          
              126  SETUP_FINALLY       140  'to 140'

 L.  41       128  POP_BLOCK        
              130  POP_EXCEPT       
              132  CALL_FINALLY        140  'to 140'
              134  JUMP_ABSOLUTE       156  'to 156'
              136  POP_BLOCK        
              138  BEGIN_FINALLY    
            140_0  COME_FROM           132  '132'
            140_1  COME_FROM_FINALLY   126  '126'
              140  LOAD_CONST               None
              142  STORE_FAST               'exc'
              144  DELETE_FAST              'exc'
              146  END_FINALLY      
              148  POP_EXCEPT       
              150  JUMP_BACK            20  'to 20'
            152_0  COME_FROM           118  '118'
              152  END_FINALLY      
              154  JUMP_BACK            20  'to 20'
            156_0  COME_FROM            26  '26'

 L.  42       156  LOAD_FAST                'cls'
              158  LOAD_FAST                'topics'
              160  CALL_FUNCTION_1       1  ''
              162  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 132

    def __repr__(self):
        return type(self).__name__ + '(topics={0!r})'.formatself.topics


class SubscribePacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = SubscribePayload

    def __init__(self, fixed=None, variable_header=None, payload=None):
        if fixed is None:
            header = MQTTFixedHeader(SUBSCRIBE, 2)
        else:
            if fixed.packet_type is not SUBSCRIBE:
                raise HBMQTTException('Invalid fixed packet type %s for SubscribePacket init' % fixed.packet_type)
            header = fixed
        super().__init__header
        self.variable_header = variable_header
        self.payload = payload

    @classmethod
    def build(cls, topics, packet_id):
        v_header = PacketIdVariableHeader(packet_id)
        payload = SubscribePayload(topics)
        return SubscribePacket(variable_header=v_header, payload=payload)