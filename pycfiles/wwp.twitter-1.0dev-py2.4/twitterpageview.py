# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/twitter/browser/twitterpageview.py
# Compiled at: 2009-08-07 09:03:36
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from wwp.twitter import twitterMessageFactory as _
import twitter, find_urls, simplejson, urllib, datetime

class ItwitterpageView(Interface):
    """
    twitterpage view interface
    """
    __module__ = __name__

    def test():
        """ test method"""
        pass


class twitterpageView(BrowserView):
    """
    twitterpage browser view
    """
    __module__ = __name__
    implements(ItwitterpageView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def twitter_posts(self):
        api = twitter.Api(username=self.context.username)
        statuses = api.GetUserTimeline(self.context.username)
        statuses = statuses[:self.context.numbertodisp]
        status_output = []
        for s in statuses:
            s = find_urls.fix_urls(s.text)
            status_output.append(s)

        return status_output

    def test(self):
        """
        test method
        """
        dummy = _('a dummy string')
        return {'dummy': dummy}