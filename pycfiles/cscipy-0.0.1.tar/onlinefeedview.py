# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/csci/tweetsite/browser/onlinefeedview.py
# Compiled at: 2009-11-13 08:52:58
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from csci.tweetsite import tweetsiteMessageFactory as _
from Products.CMFCore.utils import getToolByName

class IonlineFeedView(Interface):
    """
    onlineFeed view interface
    """
    __module__ = __name__

    def test():
        """ test method"""
        pass


class onlineFeedView(BrowserView):
    """
    onlineFeed browser view
    """
    __module__ = __name__
    implements(IonlineFeedView)

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