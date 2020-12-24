# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kssinline/browser/viewlets/calendar.py
# Compiled at: 2008-10-02 13:12:26
"""
The module name 'calendar' is a misnomer.

Archetypes widgets attempt to put CSS and Javascript resources in slots,
but since the idea of collective.kssinline is to not reload pages these 
resources are not available resulting in Javascript errors on widgets.

Until we find a better way we simply dynamically include all known AT CSS
and Javascript.
"""
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