# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/recentactivity.py
# Compiled at: 2010-05-19 10:20:52
import time
from datetime import datetime
from utils import compute_time
import logging, Globals, os.path
from AccessControl import getSecurityManager, ClassSecurityInfo
from Products.Five import BrowserView
from zope.component import getUtility
from plone.memoize.instance import memoize
from Acquisition import aq_parent
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from collective.portlet.recentactivity.interfaces import IRecentActivityUtility
from zope.component import getUtility
from collective.portlet.recentactivity.interfaces import IRecentActivityUtility

class RecentActivityView(BrowserView):
    __module__ = __name__
    template = ViewPageTemplateFile('recentactivity.pt')
    try:
        template.id = '@@recent-activity'
    except AttributeError:
        pass

    def __call__(self):
        """View the recent activity on a separate page.
        """
        self.request.set('disable_border', True)
        return self.template()

    @memoize
    def recent_activities(self):
        context = aq_inner(self.context)
        activities = getUtility(IRecentActivityUtility)
        return [ dict(time=compute_time(int(time.time()) - activity[0]), action=activity[1]['action'], user=activity[1]['user'], user_url='%s/author/%s' % (context.portal_url(), activity[1]['user']), object=activity[1]['object'], object_url=activity[1]['object_url'], parent=activity[1]['parent'], parent_url=activity[1]['parent_url']) for activity in activities.getRecentActivity(100) ]

    def have_activities(self):
        return len(self.activities()) > 0