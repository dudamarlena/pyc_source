# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/sectionsubskin/traverser.py
# Compiled at: 2008-07-18 06:49:04
from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter, queryMultiAdapter
from zope.app.publisher.browser import getDefaultViewName
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.http import IHTTPRequest
try:
    from ZPublisher.BaseRequest import DefaultPublishTraverse
    _ZOPE29 = False
except:
    from zope.app.traversing.adapters import DefaultTraversable as DefaultPublishTraverse
    from Products.ATContentTypes.content.folder import ATFolder
    _ZOPE29 = True

from zope.event import notify
from Products.ATContentTypes.interface import IATFolder
from collective.sectionsubskin.interfaces import ITraverseThroughEvent

class NotifyingTraverser(DefaultPublishTraverse):
    __module__ = __name__

    def __init__(self, context, request):
        self.subpath = []
        self.klass = None
        return super(NotifyingTraverser, self).__init__(context, request)

    def publishTraverse(self, request, name):
        notify(TraverseThroughEvent(self.context.aq_inner, request))
        return self.getViewOrTraverse(request, name)

    def getViewOrTraverse(self, request, name):
        view = queryMultiAdapter((self.context, request), name=name)
        if view is not None:
            try:
                return view.__of__(self.context)
            except AttributeError:
                return view

        return super(NotifyingTraverser, self).publishTraverse(request, name)


if _ZOPE29:

    def _ZOPE29BOBO__bobo_traverse__(self, REQUEST, name):
        """Allows transparent access to session subobjects.
        """
        RESPONSE = getattr(REQUEST, 'RESPONSE', None)
        notify(TraverseThroughEvent(self.aq_inner, REQUEST))
        data = self.getSubObject(name, REQUEST, RESPONSE)
        if data is not None:
            return data
        target = None
        method = REQUEST.get('REQUEST_METHOD', 'GET').upper()
        if len(REQUEST.get('TraversalRequestNameStack', ())) == 0 and method not in ('GET',
                                                                                     'HEAD',
                                                                                     'POST'):
            if shasattr(self, name):
                target = getattr(self, name)
        else:
            target = getattr(self, name, None)
        if target is None:
            view = queryMultiAdapter((self, REQUEST), name=name)
            if view is not None:
                target = view
        if target is None and method not in ('GET', 'POST') and not isinstance(RESPONSE, xmlrpc.Response) and REQUEST.maybe_webdav_client:
            return NullResource(self, name, REQUEST).__of__(self)
        raise AttributeError(name)
        return


    ATFolder.__bobo_traverse__ = _ZOPE29BOBO__bobo_traverse__

class TraverseThroughEvent(object):
    """An event which gets sent when traversal passes through an object"""
    __module__ = __name__
    implements(ITraverseThroughEvent)

    def __init__(self, ob, request):
        self.object = ob
        self.request = request
        super(TraverseThroughEvent, self).__init__(ob, request)