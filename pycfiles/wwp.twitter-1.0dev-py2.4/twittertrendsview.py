# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/twitter/browser/twittertrendsview.py
# Compiled at: 2009-08-20 08:07:31
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from wwp.twitter import twitterMessageFactory as _
import twitter, find_urls, simplejson, urllib, datetime
from Products.statusmessages.interfaces import IStatusMessage

class ItwittertrendsView(Interface):
    """
    twittertrends view interface
    """
    __module__ = __name__

    def test():
        """ test method"""
        pass


class twittertrendsView(BrowserView):
    """
    twittertrends browser view
    """
    __module__ = __name__
    implements(ItwittertrendsView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def twitter_trends(self):
        if hasattr(self.context, 'trends_info'):
            return self.context.trends_info
        else:
            return 'no trends posted yet'

    def test(self):
        """
        test method
        """
        dummy = _('a dummy string')
        return {'dummy': dummy}