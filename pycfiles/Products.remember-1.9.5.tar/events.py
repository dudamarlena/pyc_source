# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/events.py
# Compiled at: 2008-09-11 19:48:09
__author__ = 'Jens Klein <jens@bluedynamics.com>'
__docformat__ = 'plaintext'
from zope.interface import implements, Interface, Attribute

class IRelationEvent(Interface):
    """An generic event related to a Relation.

    The references are all from one single Relation.
    """
    __module__ = __name__
    context = Attribute('The context')
    references = Attribute('A list of references')


class IRelationConnectedEvent(IRelationEvent):
    """An event related to a Relation connection."""
    __module__ = __name__


class IRelationDisconnectedEvent(IRelationEvent):
    """An event related to a Relation disconnection."""
    __module__ = __name__


class RelationEvent(object):
    """connect happend."""
    __module__ = __name__
    implements(IRelationEvent)

    def __init__(self, context, references):
        self.context = context
        self.references = references


class RelationConnectedEvent(RelationEvent):
    """connect happend."""
    __module__ = __name__
    implements(IRelationConnectedEvent)


class RelationDisconnectedEvent(RelationEvent):
    """disconnect happend."""
    __module__ = __name__
    implements(IRelationDisconnectedEvent)