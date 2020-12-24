# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-target-g7omgaxk/lib/python/yaml/nodes.py
# Compiled at: 2018-06-28 19:00:20
# Size of source mod 2**32: 1440 bytes


class Node(object):

    def __init__(self, tag, value, start_mark, end_mark):
        self.tag = tag
        self.value = value
        self.start_mark = start_mark
        self.end_mark = end_mark

    def __repr__(self):
        value = self.value
        value = repr(value)
        return '%s(tag=%r, value=%s)' % (self.__class__.__name__, self.tag, value)


class ScalarNode(Node):
    id = 'scalar'

    def __init__(self, tag, value, start_mark=None, end_mark=None, style=None):
        self.tag = tag
        self.value = value
        self.start_mark = start_mark
        self.end_mark = end_mark
        self.style = style


class CollectionNode(Node):

    def __init__(self, tag, value, start_mark=None, end_mark=None, flow_style=None):
        self.tag = tag
        self.value = value
        self.start_mark = start_mark
        self.end_mark = end_mark
        self.flow_style = flow_style


class SequenceNode(CollectionNode):
    id = 'sequence'


class MappingNode(CollectionNode):
    id = 'mapping'