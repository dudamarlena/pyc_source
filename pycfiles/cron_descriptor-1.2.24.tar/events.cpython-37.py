# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-target-g7omgaxk/lib/python/yaml/events.py
# Compiled at: 2018-06-28 19:00:20
# Size of source mod 2**32: 2445 bytes


class Event(object):

    def __init__(self, start_mark=None, end_mark=None):
        self.start_mark = start_mark
        self.end_mark = end_mark

    def __repr__(self):
        attributes = [key for key in ('anchor', 'tag', 'implicit', 'value') if hasattr(self, key)]
        arguments = ', '.join(['%s=%r' % (key, getattr(self, key)) for key in attributes])
        return '%s(%s)' % (self.__class__.__name__, arguments)


class NodeEvent(Event):

    def __init__(self, anchor, start_mark=None, end_mark=None):
        self.anchor = anchor
        self.start_mark = start_mark
        self.end_mark = end_mark


class CollectionStartEvent(NodeEvent):

    def __init__(self, anchor, tag, implicit, start_mark=None, end_mark=None, flow_style=None):
        self.anchor = anchor
        self.tag = tag
        self.implicit = implicit
        self.start_mark = start_mark
        self.end_mark = end_mark
        self.flow_style = flow_style


class CollectionEndEvent(Event):
    pass


class StreamStartEvent(Event):

    def __init__(self, start_mark=None, end_mark=None, encoding=None):
        self.start_mark = start_mark
        self.end_mark = end_mark
        self.encoding = encoding


class StreamEndEvent(Event):
    pass


class DocumentStartEvent(Event):

    def __init__(self, start_mark=None, end_mark=None, explicit=None, version=None, tags=None):
        self.start_mark = start_mark
        self.end_mark = end_mark
        self.explicit = explicit
        self.version = version
        self.tags = tags


class DocumentEndEvent(Event):

    def __init__(self, start_mark=None, end_mark=None, explicit=None):
        self.start_mark = start_mark
        self.end_mark = end_mark
        self.explicit = explicit


class AliasEvent(NodeEvent):
    pass


class ScalarEvent(NodeEvent):

    def __init__(self, anchor, tag, implicit, value, start_mark=None, end_mark=None, style=None):
        self.anchor = anchor
        self.tag = tag
        self.implicit = implicit
        self.value = value
        self.start_mark = start_mark
        self.end_mark = end_mark
        self.style = style


class SequenceStartEvent(CollectionStartEvent):
    pass


class SequenceEndEvent(CollectionEndEvent):
    pass


class MappingStartEvent(CollectionStartEvent):
    pass


class MappingEndEvent(CollectionEndEvent):
    pass