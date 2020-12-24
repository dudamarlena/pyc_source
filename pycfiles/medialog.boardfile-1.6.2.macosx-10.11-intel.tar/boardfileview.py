# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/medialog/boardfile/browser/boardfileview.py
# Compiled at: 2011-10-07 04:21:09
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
from medialog.boardfile import boardfileMessageFactory as _

class IBoardfileView(Interface):
    """
    boardfile view interface
    """

    def test():
        """ test method"""
        pass


class BoardfileView(BrowserView):
    """
    boardfile browser view
    """
    implements(IBoardfileView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _('a dummy string')
        return {'dummy': dummy}