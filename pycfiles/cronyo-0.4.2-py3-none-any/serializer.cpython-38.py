# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/yaml/serializer.py
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
        else:
            if self.closed:
                raise SerializerError('serializer is closed')
            else:
                raise SerializerError('serializer is already opened')

    def close(self):
        if self.closed is None:
            raise SerializerError('serializer is not opened')
        else:
            if not self.closed:
                self.emit(StreamEndEvent())
                self.closed = True

    def serialize(self, node):
        if self.closed is None:
            raise SerializerError('serializer is not opened')
        else:
            if self.closed:
                raise SerializerError('serializer is closed')
        self.emit(DocumentStartEvent(explicit=(self.use_explicit_start), version=(self.use_version),
          tags=(self.use_tags)))
        self.anchor_node(node)
        self.serialize_node(node, None, None)
        self.emit(DocumentEndEvent(explicit=(self.use_explicit_end)))
        self.serialized_nodes = {}
        self.anchors = {}
        self.last_anchor_id = 0

    def anchor_node(self, node):
        if node in self.anchors:
            if self.anchors[node] is None:
                self.anchors[node] = self.generate_anchor(node)
        else:
            self.anchors[node] = None
            if isinstance(node, SequenceNode):
                for item in node.value:
                    self.anchor_node(item)

            else:
                if isinstance(node, MappingNode):
                    for key, value in node.value:
                        self.anchor_node(key)
                        self.anchor_node(value)

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
            else:
                if isinstance(node, SequenceNode):
                    implicit = node.tag == self.resolve(SequenceNode, node.value, True)
                    self.emit(SequenceStartEvent(alias, (node.tag), implicit, flow_style=(node.flow_style)))
                    index = 0
                    for item in node.value:
                        self.serialize_node(item, node, index)
                        index += 1
                    else:
                        self.emit(SequenceEndEvent())

                else:
                    if isinstance(node, MappingNode):
                        implicit = node.tag == self.resolve(MappingNode, node.value, True)
                        self.emit(MappingStartEvent(alias, (node.tag), implicit, flow_style=(node.flow_style)))
                        for key, value in node.value:
                            self.serialize_node(key, node, None)
                            self.serialize_node(value, node, key)
                        else:
                            self.emit(MappingEndEvent())

            self.ascend_resolver()