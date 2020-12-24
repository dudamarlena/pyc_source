# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/browser/publisher.py
# Compiled at: 2009-05-04 14:30:04
from zope.location import LocationProxy
from zope.publisher.interfaces import browser, NotFound
from zope.component import queryMultiAdapter, getSiteManager
from zope.component.interfaces import ComponentLookupError, IDefaultViewName
from zope.interface import implements, providedBy

class TemplatesPublisher(object):
    __module__ = __name__
    implements(browser.IBrowserPublisher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        for (n, adapter) in self.context.getAllTemplates():
            if n == name:
                return LocationProxy(adapter, container=self.context, name=name)

        view = queryMultiAdapter((self.context, request), name=name)
        if view is not None:
            return view
        raise NotFound(self.context, name, request)
        return

    def browserDefault(self, request):
        name = getSiteManager(self.context).adapters.lookup(map(providedBy, (object, request)), IDefaultViewName)
        if name is not None:
            return (
             self.context, (name,))
        raise ComponentLookupError("Couldn't find default view name", self.context, request)
        return