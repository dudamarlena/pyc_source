# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/site.py
# Compiled at: 2012-06-20 10:07:04
__docformat__ = 'restructuredtext'
from zope.intid.interfaces import IIntIds
from ztfy.utils.interfaces import INewSiteManagerEvent
from zope.component import getUtility
from zope.interface import implements
from zope.location import locate

class NewSiteManagerEvent(object):
    """Event notified when a new site manager is created"""
    implements(INewSiteManagerEvent)

    def __init__(self, obj):
        self.object = obj


def locateAndRegister(contained, parent, key, intids=None):
    locate(contained, parent)
    if intids is None:
        intids = getUtility(IIntIds)
    intids.register(contained)
    parent[key] = contained
    return