# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/database.py
# Compiled at: 2012-06-20 11:58:15
__docformat__ = 'restructuredtext'
import transaction
from zope.catalog.interfaces import ICatalog
from zope.component.interfaces import IComponentRegistry, ISite
from zope.intid.interfaces import IIntIds
from zope.processlifetime import IDatabaseOpenedWithRoot
from ztfy.security.interfaces import ILocalRoleIndexer
from ztfy.utils.interfaces import INewSiteManagerEvent
from zc.catalog.catalogindex import SetIndex
from zope.app.publication.zopepublication import ZopePublication
from zope.catalog.catalog import Catalog
from zope.component import adapter, queryUtility
from zope.intid import IntIds
from zope.location import locate
from zope.site import hooks
from ztfy.security.indexer import ALL_ROLES_INDEX_NAME
from ztfy.utils.site import locateAndRegister

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
    catalog = default.get('SecurityCatalog')
    if catalog is None:
        catalog = Catalog()
        locateAndRegister(catalog, default, 'SecurityCatalog', intids)
        IComponentRegistry(sm).registerUtility(catalog, ICatalog, 'SecurityCatalog')
    if catalog is not None:
        if ALL_ROLES_INDEX_NAME not in catalog:
            index = SetIndex(ALL_ROLES_INDEX_NAME, ILocalRoleIndexer, False)
            locateAndRegister(index, catalog, ALL_ROLES_INDEX_NAME, intids)
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