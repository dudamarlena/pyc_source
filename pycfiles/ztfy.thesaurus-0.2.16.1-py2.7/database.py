# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/database.py
# Compiled at: 2013-04-16 04:13:24
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
        if 'ztfy.ThesaurusManager' not in catalog:
            index = SetIndex('ztfy.ThesaurusManager', ILocalRoleIndexer, False)
            locateAndRegister(index, catalog, 'ztfy.ThesaurusManager', intids)
        if 'ztfy.ThesaurusContentManager' not in catalog:
            index = SetIndex('ztfy.ThesaurusContentManager', ILocalRoleIndexer, False)
            locateAndRegister(index, catalog, 'ztfy.ThesaurusContentManager', intids)
        if 'ztfy.ThesaurusExtractManager' not in catalog:
            index = SetIndex('ztfy.ThesaurusExtractManager', ILocalRoleIndexer, False)
            locateAndRegister(index, catalog, 'ztfy.ThesaurusExtractManager', intids)
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