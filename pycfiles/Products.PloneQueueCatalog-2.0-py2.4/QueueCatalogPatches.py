# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/PloneQueueCatalog/QueueCatalogPatches.py
# Compiled at: 2007-12-14 20:30:01
import sys
from AccessControl import getSecurityManager, ClassSecurityInfo
try:
    from Products.CMFCore.permissions import View
except ImportError:
    from Products.CMFCore.CMFCorePermissions import View

from AccessControl.Permissions import manage_zcatalog_entries
from AccessControl.Permissions import view_management_screens
from Products.QueueCatalog import QueueCatalog
_zcatalog_methods = {'manage_addIndex': 1, 'delIndex': 1, 'addIndex': 1, 'manage_addColumn': 1, 'delColumn': 1, 'addColumn': 1, 'getIndexObjects': 1, 'unrestrictedSearchResults': 1, 'manage_convertIndexes': 1, 'catalog_object': 0, '_listAllowedRolesAndUsers': 1, 'migrateIndexes': 1, '_createTextIndexes': 1, '_removeIndex': 1, 'enumerateIndexes': 1, 'enumerateColumns': 1, 'enumerateLexicons': 1, 'getCounter': 1}
module = sys.modules[QueueCatalog.__module__]
module._zcatalog_methods.update(_zcatalog_methods)

def indexObject(self, object, idxs=[]):
    """Add to catalog. Patched to allow specifying indexes
    """
    self.catalog_object(object, self.uidForObject(object), idxs)


patch1 = 0
if not hasattr(QueueCatalog, '_qc_indexObject'):
    from Products.QueueCatalog import QueueCatalog
    QueueCatalog._qc_indexObject = QueueCatalog.indexObject
    QueueCatalog.indexObject = indexObject
    security = getattr(QueueCatalog, 'security', ClassSecurityInfo())
    security.declarePrivate('indexObject')
    security.apply(QueueCatalog)
    patch1 = 1

def catalog_object(self, obj, uid=None, idxs=None, update_metadata=1, pghandler=None):
    """Patched to allow specifying indexes as in the plone catalog tool,
    update_metadata and pghandler. Discard pghandler for now
    """
    self._qc_catalog_object(obj, uid=uid, idxs=idxs, update_metadata=update_metadata)
    obj._p_deactivate()


patch2 = 0
if not hasattr(QueueCatalog, '_qc_catalog_object'):
    from Products.QueueCatalog import QueueCatalog
    QueueCatalog._qc_catalog_object = QueueCatalog.catalog_object
    QueueCatalog.catalog_object = catalog_object
    security = getattr(QueueCatalog, 'security', ClassSecurityInfo())
    security.declareProtected(manage_zcatalog_entries, 'catalog_object')
    security.apply(QueueCatalog)
    patch2 = 1
patch3 = 0
if not hasattr(QueueCatalog, 'readonly_while_indexing'):
    from Products.QueueCatalog import QueueCatalog
    QueueCatalog.readonly_while_indexing = False
    patch3 = 1

def reindexObject(self, object, idxs=[], update_metadata=1, uid=None):
    """Update catalog after object data has changed.

    Patched to allow update_metadata
    """
    self.catalog_object(object, uid or self.uidForObject(object), idxs=idxs, update_metadata=update_metadata)


patch4 = 0
if not hasattr(QueueCatalog, '_qc_reindexObject'):
    from Products.QueueCatalog import QueueCatalog
    QueueCatalog._qc_reindexObject = QueueCatalog.reindexObject
    QueueCatalog.reindexObject = reindexObject
    security = getattr(QueueCatalog, 'security', ClassSecurityInfo())
    security.declarePrivate('reindexObject')
    security.apply(QueueCatalog)
    patch4 = 1