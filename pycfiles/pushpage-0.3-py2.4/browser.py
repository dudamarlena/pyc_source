# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pushpage/browser.py
# Compiled at: 2006-10-05 16:04:27
""" Class:  PushPage

$Id: browser.py,v 1.7 2006/10/05 20:04:27 tseaver Exp $
"""
from zope.event import notify
from zope.interface import implements
from zope.pagetemplate.pagetemplate import PageTemplate
from zope.publisher.interfaces.browser import IBrowserPublisher
from pushpage.events import PushPageNamespaceInit
from pushpage.events import PushPageRendered

class PushPageTemplate(PageTemplate):
    __module__ = __name__

    def pt_getContext(self, args=(), options={}, **ignored):
        return options


class PushPage:
    __module__ = __name__
    implements(IBrowserPublisher)

    def __init__(self, context, request, template, mapper):
        self.context = context
        self.request = request
        self.template = template
        self.mapper = mapper

    def browserDefault(self, request):
        return (
         self, ())

    def publishTraverse(self, request, name):
        if name == 'index.html':
            return self.index
        raise NotFound(self, name, request)

    def __call__(self):
        namespace = self.mapper(self.context, self.request)
        notify(PushPageNamespaceInit(self, namespace))
        rendered = self.template(**namespace)
        notify(PushPageRendered(self, rendered))
        return rendered


class PushPageFactory:
    __module__ = __name__
    page_class = PushPage

    def __init__(self, template, mapper, checker=None):
        if getattr(template, 'read', None) is not None:
            template = template.read()
        self.template = PushPageTemplate()
        self.template.write(template)
        self.mapper = mapper
        self.checker = checker
        return

    def __call__(self, context, request):
        page = self.page_class(context, request, self.template, self.mapper)
        if self.checker is not None:
            page.__Security_checker__ = self.checker
        return page