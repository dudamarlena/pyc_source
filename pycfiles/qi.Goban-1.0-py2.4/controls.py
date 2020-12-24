# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/browser/controls.py
# Compiled at: 2008-04-06 04:02:04
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from qi.Goban.interfaces import IGoGame
from qi.Goban import GobanMessageFactory as _

class GobanControlsViewlet(BrowserView):
    """Viewlet that displays controls for the goban
        """
    __module__ = __name__
    implements(IViewlet)
    render = ViewPageTemplateFile('controls.pt')

    def __init__(self, context, request, view, manager):
        super(GobanControlsViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.view = view
        self.manager = manager
        self.gogame = IGoGame(self.context)