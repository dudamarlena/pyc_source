# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/interfaces.py
# Compiled at: 2010-05-19 10:20:52
from zope import schema
from zope.interface import Interface, Attribute
from plone.portlets.interfaces import IPortletDataProvider
from collective.portlet.recentactivity import RecentActivityPortletMessageFactory as _

class IRecentActivityPortlet(IPortletDataProvider):
    __module__ = __name__
    count = schema.Int(title=_('Number of items to display'), description=_('How many items to list.'), required=True, default=5)


class IRecentActivityUtility(Interface):
    """ Utility to store recent activity.
    """
    __module__ = __name__

    def addActivity(timestamp, action, user, object, parent):
        """Add an activity to the log.
        """
        pass

    def getRecentActivity(items):
        """Get recent activities.
        """
        pass