# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/pluggabletemplates/baseview.py
# Compiled at: 2006-11-01 08:19:33
__docformat__ = 'reStructuredText'
from zope import interface
from zope import component
from zope.pagetemplate.interfaces import IPageTemplate
from zope.publisher.browser import BrowserView
from interfaces import ITemplatedContentProvider

class TemplatedContentProvider(object):
    __module__ = __name__
    interface.implements(ITemplatedContentProvider)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self):
        pass

    def render(self):
        return self.template()


class BaseView(TemplatedContentProvider, BrowserView):
    __module__ = __name__

    def __call__(self):
        self.update()
        return self.render()


class MasterTemplatedContentProvider(TemplatedContentProvider):
    __module__ = __name__

    def render(self):
        return self.master()


class MasterView(MasterTemplatedContentProvider, BrowserView):
    __module__ = __name__

    def __call__(self):
        self.update()
        return self.render()