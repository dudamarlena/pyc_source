# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/ely/advancedquery/utility.py
# Compiled at: 2008-06-10 17:05:54
from DateTime import DateTime
from zope.interface import implements
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.CMFCore.utils import _getAuthenticatedUser
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.permissions import AccessInactivePortalContent
from Products.AdvancedQuery import Eq, Between, Le, In
from ely.advancedquery.interfaces import IAdvancedCatalogQuery

class AdvancedCatalogQuery(object):
    __module__ = __name__
    implements(IAdvancedCatalogQuery)

    def __call__(self, query, sort_specs=(), show_inactive=False):
        """Calls ZCatalog.evalAdvancedQuery
        """
        portal = getUtility(ISiteRoot)
        catalog = getToolByName(portal, 'portal_catalog')
        user = _getAuthenticatedUser(catalog)
        query = query & In('allowedRolesAndUsers', catalog._listAllowedRolesAndUsers(user))
        if not show_inactive:
            now = DateTime()
            query = query & Le('effective', now, filter=True)
        return catalog.evalAdvancedQuery(query, sortSpecs=sort_specs)