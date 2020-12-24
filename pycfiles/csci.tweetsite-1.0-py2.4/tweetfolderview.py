# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/csci/tweetsite/browser/tweetfolderview.py
# Compiled at: 2009-11-19 05:44:51
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from csci.tweetsite import tweetsiteMessageFactory as _
import datetime, time

class ItweetfolderView(Interface):
    """
    tweetfolder view interface
    """
    __module__ = __name__

    def test():
        """ test method"""
        pass

    def sort_content():
        """ sort folder contents """
        pass


class tweetfolderView(BrowserView):
    """
    tweetfolder browser view
    """
    __module__ = __name__
    implements(ItweetfolderView)

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

    def next(self):
        if hasattr(self.request, 'page'):
            self.context.page += 1
            print self.context.page

    def sort_content(self, objects):
        obj_list = []
        for obj in objects:
            created_dt = str(obj.creation_date)[:19]
            created_dt = time.strptime(created_dt, '%Y/%m/%d %H:%M:%S')
            created_time = time.gmtime(float(time.mktime(created_dt)))
            created_time = time.strftime('%Y/%m/%d %H:%M', created_time)
            obj_list.append((created_time, obj))

        obj_list.sort(reverse=True)
        return obj_list