# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/database.py
# Compiled at: 2012-06-26 16:39:45
__docformat__ = 'restructuredtext'
import transaction
from zope.catalog.interfaces import ICatalog
from zope.component.interfaces import IComponentRegistry, ISite
from zope.intid.interfaces import IIntIds
from zope.processlifetime import IDatabaseOpenedWithRoot
from ztfy.gallery.interfaces import IGalleryImage
from ztfy.utils.interfaces import INewSiteManagerEvent
from zope.app.publication.zopepublication import ZopePublication
from zope.catalog.catalog import Catalog
from zope.component import adapter, queryUtility
from zope.intid import IntIds
from zope.location import locate
from zope.site import hooks
from ztfy.utils.catalog.index import TextIndexNG
from ztfy.utils.site import locateAndRegister

def updateDatabaseIfNeeded(context):
    """Check for missing objects at application startup"""
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
            default['IntIds'] = intids
            IComponentRegistry(sm).registerUtility(intids, IIntIds)
    catalog = default.get('Catalog')
    if catalog is None:
        catalog = Catalog()
        locateAndRegister(catalog, default, 'Catalog', intids)
        IComponentRegistry(sm).registerUtility(catalog, ICatalog, 'Catalog')
    if catalog is not None:
        if 'image_title' not in catalog:
            index = TextIndexNG('title description', IGalleryImage, False, languages='fr en', storage='txng.storages.term_frequencies', dedicated_storage=False, use_stopwords=True, use_normalizer=True, ranking=True)
            locateAndRegister(index, catalog, 'image_title', intids)
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