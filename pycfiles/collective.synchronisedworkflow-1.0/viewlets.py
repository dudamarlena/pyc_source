# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/sylvester/browser/viewlets.py
# Compiled at: 2009-07-07 15:44:39
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Friendlet(BrowserView):
    __module__ = __name__
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.__parent__ = view
        self.manager = manager

    def update(self):
        pass

    render = ViewPageTemplateFile('templates/friendlet.pt')


class Statuslet(BrowserView):
    __module__ = __name__
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.__parent__ = view
        self.manager = manager

    def update(self):
        pass

    render = ViewPageTemplateFile('templates/statuslet.pt')