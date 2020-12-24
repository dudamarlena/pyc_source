# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/z2utils/indexing.py
# Compiled at: 2007-11-30 08:40:13
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone import CatalogTool
from zope import interface
from p4a.z2utils.utils import interfaceToName
if not hasattr(CatalogTool, 'object_provides'):

    def object_provides(object, portal, **kw):
        """Returns a list of strings representing all interfaces provided by
        an object.

        """
        return [ interfaceToName(portal, i) for i in interface.providedBy(object).flattened() ]


    CatalogTool.registerIndexableAttribute('object_provides', object_provides)

def ensure_object_provides(context):
    """Make sure the closest catalog to context has an index representing
    the object_provides index.
    """
    catalog = cmfutils.getToolByName(context, 'portal_catalog')
    if 'object_provides' not in catalog.indexes():
        catalog.manage_addIndex('object_provides', 'KeywordIndex')
        catalog.manage_reindexIndex('object_provides')