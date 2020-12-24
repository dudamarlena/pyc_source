# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/browser/viewlets/calendar.py
# Compiled at: 2008-10-02 13:12:26
__doc__ = "\nThe module name 'calendar' is a misnomer.\n\nArchetypes widgets attempt to put CSS and Javascript resources in slots,\nbut since the idea of collective.kssinline is to not reload pages these \nresources are not available resulting in Javascript errors on widgets.\n\nUntil we find a better way we simply dynamically include all known AT CSS\nand Javascript.\n"
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Calendar(BrowserView):
    __module__ = __name__
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.__parent__ = view
        self.manager = manager

    def update(self):
        pass

    render = ViewPageTemplateFile('calendar.pt')