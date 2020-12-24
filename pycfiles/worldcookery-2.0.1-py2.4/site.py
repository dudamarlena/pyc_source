# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/site.py
# Compiled at: 2006-09-21 05:27:35
from zope.interface import implements
from zope.component import adapter
from zope.event import notify
from zope.app.container.btree import BTreeContainer
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.component.site import SiteManagerContainer, LocalSiteManager
from worldcookery.interfaces import IWorldCookerySite
from worldcookery.interfaces import INewWorldCookerySiteEvent

class NewWorldCookerySiteEvent(object):
    __module__ = __name__
    implements(INewWorldCookerySiteEvent)

    def __init__(self, site):
        self.object = site


class WorldCookerySite(SiteManagerContainer, BTreeContainer):
    __module__ = __name__
    implements(IWorldCookerySite)

    def setSiteManager(self, sm):
        super(WorldCookerySite, self).setSiteManager(sm)
        notify(NewWorldCookerySiteEvent(self))


@adapter(IWorldCookerySite, IObjectAddedEvent)
def setSiteManagerWhenAdded(site, event):
    site.setSiteManager(LocalSiteManager(site))