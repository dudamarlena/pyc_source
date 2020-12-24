# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-target-g7omgaxk/lib/python/yaml/serializer.py
# Compiled at: 2018-06-28 19:00:20
# Size of source mod 2**32: 4165 bytes
__all__ = ['Serializer', 'SerializerError']
from .error import YAMLError
from .events import *
from .nodes import *

class SerializerError(YAMLError):
    pass


class Serializer:
    ANCHOR_TEMPLATE = 'id%03d'

    def __init__(self, encoding=None, explicit_start=None, explicit_end=None, version=None, tags=None):
        self.use_encoding = encoding
        self.use_explicit_start = explicit_start
        self.use_explicit_end = explicit_end
        self.use_version = version
        self.use_tags = tags
        self.serialized_nodes = {}
        self.anchors = {}
        self.last_anchor_id = 0
        self.closed = None

    def open(self):
        if self.closed is None:
            self.emit(StreamStartEvent(encoding=(self.use_encoding)))
            self.closed = False
        elif self.closed:
            raise SerializerError('serializer is closed')
        else:
            raise SerializerError('serializer is already opened')

    def close(self):
        if self.closed is None:
            raise SerializerError('serializer is not opened')
        elif not self.closed:
            self.emit(StreamEndEvent())
            self.closed = True

    def serialize(self, node):
        if self.closed is None:
            raise SerializerError('serializer is not opened')
        elif self.closed:
            raise SerializerError('serializer is closed')
        self.emit(DocumentStartEvent(explicit=(self.use_explicit_start), version=(self.use_version),
          tags=(self.use_tags)))
        self.anchor_node(node)
        self.serialize_node(node, None, None)
        self.emit(DocumentEndEvent(explicit=(self.use_explicit_end)))
        self.serialized_nodes = {}
        self.anchors = {}
        self.last_anchor_id = 0

    def anchor_node--- This code section failed: ---

 L.  61         0  LOAD_FAST                'node'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                anchors
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    42  'to 42'

 L.  62        10  LOAD_FAST                'self'
               12  LOAD_ATTR                anchors
               14  LOAD_FAST                'node'
               16  BINARY_SUBSCR    
               18  LOAD_CONST               None
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE   140  'to 140'

 L.  63        24  LOAD_FAST                'self'
               26  LOAD_METHOD              generate_anchor
               28  LOAD_FAST                'node'
               30  CALL_METHOD_1         1  ''
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                anchors
               36  LOAD_FAST                'node'
               38  STORE_SUBSCR     
               40  JUMP_FORWARD        140  'to 140'
             42_0  COME_FROM             8  '8'

 L.  65        42  LOAD_CONST               None
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                anchors
               48  LOAD_FAST                'node'
               50  STORE_SUBSCR     

 L.  66        52  LOAD_GLOBAL              isinstance
               54  LOAD_FAST                'node'
               56  LOAD_GLOBAL              SequenceNode
               58  CALL_FUNCTION_2       2  ''
               60  POP_JUMP_IF_FALSE    90  'to 90'

 L.  67        62  SETUP_LOOP          140  'to 140'
               64  LOAD_FAST                'node'
               66  LOAD_ATTR                value
               68  GET_ITER         
               70  FOR_ITER             86  'to 86'
               72  STORE_FAST               'item'

 L.  68        74  LOAD_FAST                'self'
               76  LOAD_METHOD              anchor_node
               78  LOAD_FAST                'item'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  JUMP_BACK            70  'to 70'
               86  POP_BLOCK        
               88  JUMP_FORWARD        140  'to 140'
             90_0  COME_FROM            60  '60'

 L.  69        90  LOAD_GLOBAL              isinstance
               92  LOAD_FAST                'node'
               94  LOAD_GLOBAL              MappingNode
               96  CALL_FUNCTION_2       2  ''
               98  POP_JUMP_IF_FALSE   140  'to 140'

 L.  70       100  SETUP_LOOP          140  'to 140'
              102  LOAD_FAST                'node'
              104  LOAD_ATTR                value
              106  GET_ITER         
              108  FOR_ITER            138  'to 138'
              110  UNPACK_SEQUENCE_2     2 
              112  STORE_FAST               'key'
              114  STORE_FAST               'value'

 L.  71       116  LOAD_FAST                'self'
              118  LOAD_METHOD              anchor_node
              120  LOAD_FAST                'key'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L.  72       126  LOAD_FAST                'self'
              128  LOAD_METHOD              anchor_node
              130  LOAD_FAST                'value'
              132  CALL_METHOD_1         1  ''
              134  POP_TOP          
              136  JUMP_BACK           108  'to 108'
              138  POP_BLOCK        
            140_0  COME_FROM_LOOP      100  '100'
            140_1  COME_FROM            98  '98'
            140_2  COME_FROM            88  '88'
            140_3  COME_FROM_LOOP       62  '62'
            140_4  COME_FROM            40  '40'
            140_5  COME_FROM            22  '22'

Parse error at or near `COME_FROM_LOOP' instruction at offset 140_3

    def generate_anchor(self, node):
        self.last_anchor_id += 1
        return self.ANCHOR_TEMPLATE % self.last_anchor_id

    def serialize_node(self, node, parent, index):
        alias = self.anchors[node]
        if node in self.serialized_nodes:
            self.emit(AliasEvent(alias))
        else:
            self.serialized_nodes[node] = True
            self.descend_resolver(parent, index)
            if isinstance(node, ScalarNode):
                detected_tag = self.resolve(ScalarNode, node.value, (True, False))
                default_tag = self.resolve(ScalarNode, node.value, (False, True))
                implicit = (node.tag == detected_tag, node.tag == default_tag)
                self.emit(ScalarEvent(alias, (node.tag), implicit, (node.value), style=(node.style)))
            elif isinstance(node, SequenceNode):
                implicit = node.tag == self.resolve(SequenceNode, node.value, True)
                self.emit(SequenceStartEvent(alias, (node.tag), implicit, flow_style=(node.flow_style)))
                index = 0
                for item in node.value:
                    self.serialize_node(item, node, index)
                    index += 1

                self.emit(SequenceEndEvent())
            elif isinstance(node, MappingNode):
                implicit = node.tag == self.resolve(MappingNode, node.value, True)
                self.emit(MappingStartEvent(alias, (node.tag), implicit, flow_style=(node.flow_style)))
                for key, value in node.value:
                    self.serialize_node(key, node, None)
                    self.serialize_node(value, node, key)

                self.emit(MappingEndEvent())
            self.ascend_resolver()