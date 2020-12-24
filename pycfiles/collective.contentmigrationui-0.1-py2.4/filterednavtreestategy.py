# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentmigrationui/browser/filterednavtreestategy.py
# Compiled at: 2010-08-19 07:17:08
from plone.app.layout.navigation.navtree import buildFolderTree, NavtreeStrategyBase
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from zope.interface import implements
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from Products.CMFCore.utils import getToolByName

class FilteredStrategyBase(DefaultNavtreeStrategy):
    """Basic navigation tree strategy that does nothing.
    """
    __module__ = __name__
    implements(INavtreeStrategy)
    __allow_access_to_unprotected_subobjects__ = 1
    rootPath = None
    showAllParents = True

    def __init__(self, context, filterType=None):
        DefaultNavtreeStrategy.__init__(self, context)
        self.filterType = filterType

    def nodeFilter(self, node):
        portalType = getattr(node['item'], 'portal_type', None)
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog.searchResults({'portal_type': self.filterType})
        pathList = [ res.getPath() for res in results ]
        for path in pathList:
            if node['item'].getPath() in path:
                return True

        return False