# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/portlet/recentactivity/utilities.py
# Compiled at: 2010-05-19 10:20:52
import time
from zope.interface import implements
from zope.app.container.btree import BTreeContainer
from OFS.SimpleItem import SimpleItem
from zope.event import notify
from BTrees.OOBTree import OOBTree
from BTrees.OIBTree import OIBTree
from persistent import Persistent
from collective.portlet.recentactivity.interfaces import IRecentActivityUtility

class RecentActivityUtility(Persistent):
    """Recent Activity Utility
    """
    __module__ = __name__
    implements(IRecentActivityUtility)
    activities = None

    def __init__(self):
        self.activities = OOBTree()

    def addActivity(self, timestamp, action, user, object, parent):
        """Add an activity to the BTree.
        """
        timestamp = int(time.time())
        activity = {'action': action, 'user': user, 'object': object, 'object_url': object.absolute_url(), 'parent': parent, 'parent_url': parent.absolute_url()}
        self.activities.insert(timestamp, activity)
        return timestamp

    def getRecentActivity(self, items=None):
        """Get all activities stored in the BTree.
        """
        if self.activities:
            if items:
                return sorted(self.activities.items(), reverse=True)[:items]
            else:
                return sorted(self.activities.items(), reverse=True)

    def manage_fixupOwnershipAfterAdd(self):
        """This is needed, otherwise we get an Attribute Error
           when we try to install the product.
        """
        pass