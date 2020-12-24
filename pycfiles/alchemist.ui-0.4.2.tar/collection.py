# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/alchemist/traversal/collection.py
# Compiled at: 2008-09-24 15:09:06
__doc__ = '\n$Id: $\n'
from zope import interface
from zope.publisher.interfaces import NotFound
from zope.location import ILocation
from zope.security.proxy import removeSecurityProxy
from z3c.traverser import interfaces

class CollectionTraverserTemplate(object):
    """A traverser that knows how to look up objects by sqlalchemy collections """
    interface.implements(interfaces.ITraverserPlugin)
    collection_attributes = ()

    def __init__(self, container, request):
        self.context = container
        self.request = request

    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.IPublishTraverse"""
        if name in self.collection_attributes:
            container = getattr(self.context, name)
            if ILocation.providedBy(container):
                trusted_ctx = removeSecurityProxy(container)
                trusted_ctx.__parent__ = self.context
                trusted_ctx.__name__ = name
            return container
        raise NotFound(self.context, name, request)


def CollectionTraverser(*names):
    return type('CollectionsTraverser', (CollectionTraverserTemplate,), {'collection_attributes': names})