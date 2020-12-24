# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/translate/browser/translatefolderview.py
# Compiled at: 2009-08-11 08:19:08
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from wwp.translate import translateMessageFactory as _

class ItranslatefolderView(Interface):
    """
    translatefolder view interface
    """
    __module__ = __name__

    def test():
        """ test method"""
        pass


class translatefolderView(BrowserView):
    """
    translatefolder browser view
    """
    __module__ = __name__
    implements(ItranslatefolderView)

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