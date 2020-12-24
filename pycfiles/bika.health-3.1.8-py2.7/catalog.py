# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/catalog.py
# Compiled at: 2014-12-12 07:13:54
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ZCatalog.ZCatalog import ZCatalog

def getCatalog(instance, field='UID'):
    """ Return the catalog which indexes objects of instance's type.
    If an object is indexed by more than one catalog, the first match
    will be returned.
    """
    uid = instance.UID()
    if 'workflow_skiplist' in instance.REQUEST and [ x for x in instance.REQUEST['workflow_skiplist'] if x.find(uid) > -1
                                                   ]:
        return
    else:
        at = getToolByName(instance, 'archetype_tool')
        plone = instance.portal_url.getPortalObject()
        catalog_name = instance.portal_type in at.catalog_map and at.catalog_map[instance.portal_type][0] or 'portal_catalog'
        catalog = getToolByName(plone, catalog_name)
        return catalog
        return


class BikaPatientCatalog(CatalogTool):
    """ Catalog for patients
    """
    security = ClassSecurityInfo()
    _properties = ({'id': 'title', 'type': 'string', 'mode': 'w'},)
    title = 'Bika Patient Catalog'
    id = 'bika_patient_catalog'
    portal_type = meta_type = 'BikaPatientCatalog'
    plone_tool = 1

    def __init__(self):
        ZCatalog.__init__(self, self.id)

    security.declareProtected(ManagePortal, 'clearFindAndRebuild')

    def clearFindAndRebuild(self):
        """
        """

        def indexObject(obj, path):
            self.reindexObject(obj)

        self.manage_catalogClear()
        portal = getToolByName(self, 'portal_url').getPortalObject()
        portal.ZopeFindAndApply(portal, obj_metatypes=('Patient', ), search_sub=True, apply_func=indexObject)


InitializeClass(BikaPatientCatalog)