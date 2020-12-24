# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/lock/database.py
# Compiled at: 2012-06-11 15:35:37
import transaction
from zope.component.interfaces import IComponentRegistry, ISite
from zope.intid.interfaces import IIntIds
from zope.processlifetime import IDatabaseOpenedWithRoot
from ztfy.lock.interfaces import ILockingUtility
from ztfy.utils.interfaces import INewSiteManagerEvent
from zope.app.publication.zopepublication import ZopePublication
from zope.component import adapter, queryUtility
from zope.intid import IntIds
from zope.location import locate
from zope.site import hooks
from ztfy.lock.utility import LockingUtility

def updateDatabaseIfNeeded(context):
    """Check for missing utilities at application startup"""
    try:
        sm = context.getSiteManager()
    except:
        return

    default = sm['default']
    intids = queryUtility(IIntIds)
    if intids is None:
        intids = default.get('IntIds')
        if intids is None:
            intids = IntIds()
            locate(intids, default)
            IComponentRegistry(sm).registerUtility(intids, IIntIds, '')
            default['IntIds'] = intids
    locker = queryUtility(ILockingUtility)
    if locker is None:
        locker = default.get('ObjectLocker')
        if locker is None:
            locker = LockingUtility()
            locate(locker, default)
            IComponentRegistry(sm).registerUtility(locker, ILockingUtility, '')
            default['ObjectLocker'] = locker
    return


@adapter(IDatabaseOpenedWithRoot)
def handleOpenedDatabase(event):
    db = event.database
    connection = db.open()
    root = connection.root()
    root_folder = root.get(ZopePublication.root_name, None)
    for site in root_folder.values():
        if ISite(site, None) is not None:
            hooks.setSite(site)
            updateDatabaseIfNeeded(site)
            transaction.commit()

    return


@adapter(INewSiteManagerEvent)
def handleNewSiteManager(event):
    updateDatabaseIfNeeded(event.object)