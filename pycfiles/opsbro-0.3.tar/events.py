# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ruamel/yaml/events.py
# Compiled at: 2017-07-27 07:36:53


def CommentCheck():
    pass


class Event(object):

    def __init__(self, start_mark=None, end_mark=None, comment=CommentCheck):
        self.start_mark = start_mark
        self.end_mark = end_mark
        if comment is CommentCheck:
            comment = None
        self.comment = comment
        return

    def __repr__(self):
        attributes = [ key for key in ['anchor', 'tag', 'implicit', 'value',
         'flow_style', 'style'] if hasattr(self, key)
                     ]
        arguments = (', ').join([ '%s=%r' % (key, getattr(self, key)) for key in attributes
                                ])
        if self.comment not in [None, CommentCheck]:
            arguments += (', comment={!r}').format(self.comment)
        return '%s(%s)' % (self.__class__.__name__, arguments)


class NodeEvent(Event):

    def __init__(self, anchor, start_mark=None, end_mark=None, comment=None):
        Event.__init__(self, start_mark, end_mark, comment)
        self.anchor = anchor


class CollectionStartEvent(NodeEvent):

    def __init__(self, anchor, tag, implicit, start_mark=None, end_mark=None, flow_style=None, comment=None):
        Event.__init__(self, start_mark, end_mark, comment)
        self.anchor = anchor
        self.tag = tag
        self.implicit = implicit
        self.flow_style = flow_style


class CollectionEndEvent(Event):
    pass


class StreamStartEvent(Event):

    def __init__(self, start_mark=None, end_mark=None, encoding=None, comment=None):
        Event.__init__(self, start_mark, end_mark, comment)
        self.encoding = encoding


class StreamEndEvent(Event):
    pass


class DocumentStartEvent(Event):

    def __init__(self, start_mark=None, end_mark=None, explicit=None, version=None, tags=None, comment=None):
        Event.__init__(self, start_mark, end_mark, comment)
        self.explicit = explicit
        self.version = version
        self.tags = tags


class DocumentEndEvent(Event):

    def __init__(self, start_mark=None, end_mark=None, explicit=None, comment=None):
        Event.__init__(self, start_mark, end_mark, comment)
        self.explicit = explicit


class AliasEvent(NodeEvent):
    pass


class ScalarEvent(NodeEvent):

    def __init__(self, anchor, tag, implicit, value, start_mark=None, end_mark=None, style=None, comment=None):
        NodeEvent.__init__(self, anchor, start_mark, end_mark, comment)
        self.tag = tag
        self.implicit = implicit
        self.value = value
        self.style = style


class SequenceStartEvent(CollectionStartEvent):
    pass


class SequenceEndEvent(CollectionEndEvent):
    pass


class MappingStartEvent(CollectionStartEvent):
    pass


class MappingEndEvent(CollectionEndEvent):
    pass