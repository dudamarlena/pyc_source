# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/database.py
# Compiled at: 2012-08-25 05:24:44
__docformat__ = 'restructuredtext'
import transaction
from hurry.workflow.interfaces import IWorkflowState
from zope.app.publication.zopepublication import ZopePublication
from zope.catalog.interfaces import ICatalog
from zope.component.interfaces import IComponentRegistry, ISite
from zope.dublincore.interfaces import IZopeDublinCore
from zope.intid.interfaces import IIntIds
from zope.processlifetime import IDatabaseOpenedWithRoot
from ztfy.utils.interfaces import INewSiteManagerEvent
from ztfy.workflow.interfaces import IWorkflowTarget
from zc.catalog.catalogindex import ValueIndex, DateTimeValueIndex
from zope.catalog.catalog import Catalog
from zope.component import adapter, queryUtility
from zope.intid import IntIds
from zope.location import locate
from zope.site import hooks
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
    catalog = default.get('WorkflowCatalog')
    if catalog is None:
        catalog = Catalog()
        locateAndRegister(catalog, default, 'WorkflowCatalog', intids)
        IComponentRegistry(sm).registerUtility(catalog, ICatalog, 'WorkflowCatalog')
    if catalog is not None:
        if 'wf_id' not in catalog:
            index = ValueIndex('getId', IWorkflowState, True)
            locateAndRegister(index, catalog, 'wf_id', intids)
        if 'wf_state' not in catalog:
            index = ValueIndex('getState', IWorkflowState, True)
            locateAndRegister(index, catalog, 'wf_state', intids)
        if 'wf_name' not in catalog:
            index = ValueIndex('workflow_name', IWorkflowTarget, False)
            locateAndRegister(index, catalog, 'wf_name', intids)
        if 'creation_date' not in catalog:
            index = DateTimeValueIndex('created', IZopeDublinCore, False)
            locateAndRegister(index, catalog, 'creation_date', intids)
        if 'modification_date' not in catalog:
            index = DateTimeValueIndex('modified', IZopeDublinCore, False)
            locateAndRegister(index, catalog, 'modification_date', intids)
        if 'effective_date' not in catalog:
            index = DateTimeValueIndex('effective', IZopeDublinCore, False)
            locateAndRegister(index, catalog, 'effective_date', intids)
        if 'expiration_date' not in catalog:
            index = DateTimeValueIndex('expires', IZopeDublinCore, False)
            locateAndRegister(index, catalog, 'expiration_date', intids)
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