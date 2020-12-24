# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ruamel/yaml/nodes.py
# Compiled at: 2017-07-27 07:36:53
from __future__ import print_function

class Node(object):

    def __init__(self, tag, value, start_mark, end_mark, comment=None):
        self.tag = tag
        self.value = value
        self.start_mark = start_mark
        self.end_mark = end_mark
        self.comment = comment
        self.anchor = None
        return

    def __repr__(self):
        value = self.value
        value = repr(value)
        return '%s(tag=%r, value=%s)' % (self.__class__.__name__,
         self.tag, value)

    def dump(self, indent=0):
        if isinstance(self.value, basestring):
            print(('{}{}(tag={!r}, value={!r})').format('  ' * indent, self.__class__.__name__, self.tag, self.value))
            if self.comment:
                print(('    {}comment: {})').format('  ' * indent, self.comment))
            return
        print(('{}{}(tag={!r})').format('  ' * indent, self.__class__.__name__, self.tag))
        if self.comment:
            print(('    {}comment: {})').format('  ' * indent, self.comment))
        for v in self.value:
            if isinstance(v, tuple):
                for v1 in v:
                    v1.dump(indent + 1)

            elif isinstance(v, Node):
                v.dump(indent + 1)
            else:
                print('Node value type?', type(v))


class ScalarNode(Node):
    """
    styles:
      ? -> set() ? key, no value
      " -> double quoted
      ' -> single quoted
      | -> literal style
      > ->
    """
    id = 'scalar'

    def __init__(self, tag, value, start_mark=None, end_mark=None, style=None, comment=None):
        Node.__init__(self, tag, value, start_mark, end_mark, comment=comment)
        self.style = style


class CollectionNode(Node):

    def __init__(self, tag, value, start_mark=None, end_mark=None, flow_style=None, comment=None, anchor=None):
        Node.__init__(self, tag, value, start_mark, end_mark, comment=comment)
        self.flow_style = flow_style
        self.anchor = anchor


class SequenceNode(CollectionNode):
    id = 'sequence'


class MappingNode(CollectionNode):
    id = 'mapping'