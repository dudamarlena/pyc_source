# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/demo/app.py
# Compiled at: 2008-12-22 07:00:12
""" Demo site
"""
__license__ = 'GPL v.3'
from zope import event
from zope.app.folder import Folder
from zope.interface import Interface, implements
from zope.app.component.site import LocalSiteManager
from ice.adverlet.interfaces import ISourceStorage, IFileStorage
from ice.adverlet.storage import SourceStorage, FileStorage

class ISite(Interface):
    """ Demo site """
    __module__ = __name__


class Site(Folder):
    __module__ = __name__
    implements(ISite)

    def __init__(self):
        super(Site, self).__init__()
        sm = LocalSiteManager(self)
        self.setSiteManager(sm)
        sm = self.getSiteManager()
        event.notify(SiteCreatedEvent(self))


class ISiteCreatedEvent(Interface):
    """ event """
    __module__ = __name__


class SiteCreatedEvent:
    __module__ = __name__
    implements(ISiteCreatedEvent)

    def __init__(self, site):
        self.site = site


def installs(e):
    site = e.site
    sm = site.getSiteManager()
    storage = SourceStorage()
    sm['adverlets_sources'] = storage
    sm.registerUtility(storage, ISourceStorage)
    storage = FileStorage()
    site['images'] = storage
    sm.registerUtility(storage, IFileStorage)