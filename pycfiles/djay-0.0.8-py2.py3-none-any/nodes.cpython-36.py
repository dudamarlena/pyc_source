# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyyaml/yaml/nodes.py
# Compiled at: 2019-07-30 18:47:04
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