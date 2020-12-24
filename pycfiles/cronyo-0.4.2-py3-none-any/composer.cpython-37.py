# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-target-g7omgaxk/lib/python/yaml/composer.py
# Compiled at: 2019-02-27 21:17:00
# Size of source mod 2**32: 4883 bytes
__all__ = ['Composer', 'ComposerError']
from .error import MarkedYAMLError
from .events import *
from .nodes import *

class ComposerError(MarkedYAMLError):
    pass


class Composer:

    def __init__(self):
        self.anchors = {}

    def check_node(self):
        if self.check_event(StreamStartEvent):
            self.get_event()
        return not self.check_event(StreamEndEvent)

    def get_node(self):
        if not self.check_event(StreamEndEvent):
            return self.compose_document()

    def get_single_node(self):
        self.get_event()
        document = None
        if not self.check_event(StreamEndEvent):
            document = self.compose_document()
        if not self.check_event(StreamEndEvent):
            event = self.get_event()
            raise ComposerError('expected a single document in the stream', document.start_mark, 'but found another document', event.start_mark)
        self.get_event()
        return document

    def compose_document(self):
        self.get_event()
        node = self.compose_node(None, None)
        self.get_event()
        self.anchors = {}
        return node

    def compose_node(self, parent, index):
        if self.check_event(AliasEvent):
            event = self.get_event()
            anchor = event.anchor
            if anchor not in self.anchors:
                raise ComposerError(None, None, 'found undefined alias %r' % anchor, event.start_mark)
        else:
            return self.anchors[anchor]
            event = self.peek_event()
            anchor = event.anchor
            if anchor is not None:
                if anchor in self.anchors:
                    raise ComposerError('found duplicate anchor %r; first occurrence' % anchor, self.anchors[anchor].start_mark, 'second occurrence', event.start_mark)
            else:
                self.descend_resolver(parent, index)
                if self.check_event(ScalarEvent):
                    node = self.compose_scalar_node(anchor)
                else:
                    if self.check_event(SequenceStartEvent):
                        node = self.compose_sequence_node(anchor)
                    else:
                        if self.check_event(MappingStartEvent):
                            node = self.compose_mapping_node(anchor)
        self.ascend_resolver()
        return node

    def compose_scalar_node(self, anchor):
        event = self.get_event()
        tag = event.tag
        if tag is None or tag == '!':
            tag = self.resolve(ScalarNode, event.value, event.implicit)
        node = ScalarNode(tag, (event.value), (event.start_mark),
          (event.end_mark), style=(event.style))
        if anchor is not None:
            self.anchors[anchor] = node
        return node

    def compose_sequence_node(self, anchor):
        start_event = self.get_event()
        tag = start_event.tag
        if tag is None or tag == '!':
            tag = self.resolve(SequenceNode, None, start_event.implicit)
        node = SequenceNode(tag, [], (start_event.start_mark),
          None, flow_style=(start_event.flow_style))
        if anchor is not None:
            self.anchors[anchor] = node
        index = 0
        while not self.check_event(SequenceEndEvent):
            node.value.append(self.compose_node(node, index))
            index += 1

        end_event = self.get_event()
        node.end_mark = end_event.end_mark
        return node

    def compose_mapping_node(self, anchor):
        start_event = self.get_event()
        tag = start_event.tag
        if tag is None or tag == '!':
            tag = self.resolve(MappingNode, None, start_event.implicit)
        node = MappingNode(tag, [], (start_event.start_mark),
          None, flow_style=(start_event.flow_style))
        if anchor is not None:
            self.anchors[anchor] = node
        while not self.check_event(MappingEndEvent):
            item_key = self.compose_node(node, None)
            item_value = self.compose_node(node, item_key)
            node.value.append((item_key, item_value))

        end_event = self.get_event()
        node.end_mark = end_event.end_mark
        return node