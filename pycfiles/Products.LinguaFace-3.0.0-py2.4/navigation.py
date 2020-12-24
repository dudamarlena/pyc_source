# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/LinguaFace/browser/navigation.py
# Compiled at: 2010-11-30 09:59:25
from Acquisition import aq_inner
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.Five import BrowserView
from Products.CMFPlone.browser.interfaces import ISiteMap
from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs
from Products.CMFPlone.browser.interfaces import INavigationTabs
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.LinguaFace.browser.navtree import buildFolderTree
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder, SitemapQueryBuilder
from Products.CMFPlone.browser.navigation import get_view_url
from Products.CMFPlone.utils import base_hasattr
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from plone.app.portlets.portlets.navigation import Renderer as oldNavigationRenderer
from plone.memoize.instance import memoize
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.interfaces import INavtreeStrategy

class Renderer(oldNavigationRenderer):
    __module__ = __name__

    @memoize
    def getNavTree(self, _marker=[]):
        context = aq_inner(self.context)
        queryBuilder = getMultiAdapter((context, self.data), INavigationQueryBuilder)
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)


class CatalogSiteMap(BrowserView):
    __module__ = __name__
    implements(ISiteMap)

    def siteMap(self):
        context = aq_inner(self.context)
        queryBuilder = SitemapQueryBuilder(context)
        query = queryBuilder()
        strategy = getMultiAdapter((context, self), INavtreeStrategy)
        return buildFolderTree(context, obj=context, query=query, strategy=strategy)


class PhysicalNavigationBreadcrumbs(BrowserView):
    __module__ = __name__
    implements(INavigationBreadcrumbs)

    def breadcrumbs(self):
        context = aq_inner(self.context)
        request = self.request
        container = utils.parent(context)
        portal_languages = getToolByName(context, 'portal_languages')
        preferredLanguage = portal_languages.getPreferredLanguage()
        if base_hasattr(context, 'getTranslation') and context.hasTranslation(preferredLanguage):
            context = context.getTranslation(preferredLanguage)
        try:
            (name, item_url) = get_view_url(context)
        except AttributeError:
            print context
            raise

        if container is None:
            return ({'absolute_url': item_url, 'Title': utils.pretty_title_or_id(context, context)},)
        view = getMultiAdapter((container, request), name='breadcrumbs_view')
        base = tuple(view.breadcrumbs())
        rootPath = getNavigationRoot(context)
        itemPath = ('/').join(context.getPhysicalPath())
        if not utils.isDefaultPage(context, request) and not rootPath.startswith(itemPath):
            base += ({'absolute_url': item_url, 'Title': utils.pretty_title_or_id(context, context)},)
        return base


class CatalogNavigationTabs(BrowserView):
    __module__ = __name__
    implements(INavigationTabs)

    def topLevelTabs(self, actions=None, category='portal_tabs'):
        """
        overriden for drop down menus products
        return canonical-path
        """
        context = aq_inner(self.context)
        portal_catalog = getToolByName(context, 'portal_catalog')
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        site_properties = getattr(portal_properties, 'site_properties')
        result = []
        if actions is not None:
            for actionInfo in actions.get(category, []):
                data = actionInfo.copy()
                data['name'] = data['title']
                result.append(data)

        if site_properties.getProperty('disable_folder_sections', False):
            return result
        customQuery = getattr(context, 'getCustomNavQuery', False)
        if customQuery is not None and utils.safe_callable(customQuery):
            query = customQuery()
        else:
            query = {}
        rootPath = getNavigationRoot(context)
        query['path'] = {'query': rootPath, 'depth': 1}
        query['portal_type'] = utils.typesToList(context)
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder
        if navtree_properties.getProperty('enable_wf_state_filtering', False):
            query['review_state'] = navtree_properties.getProperty('wf_states_to_show', [])
        query['is_default_page'] = False
        if site_properties.getProperty('disable_nonfolderish_sections', False):
            query['is_folderish'] = True
        idsNotToList = navtree_properties.getProperty('idsNotToList', ())
        excludedIds = {}
        for id in idsNotToList:
            excludedIds[id] = 1

        rawresult = portal_catalog.searchResults(**query)
        for item in rawresult:
            if not (excludedIds.has_key(item.getId) or item.exclude_from_nav):
                (id, item_url) = get_view_url(item)
                if hasattr(item, 'getCanonicalPath'):
                    canonicalPath = item.getCanonicalPath
                else:
                    canonicalPath = item.getPath()
                data = {'name': utils.pretty_title_or_id(context, item), 'id': id, 'url': item_url, 'description': item.Description, 'canonical-path': item.getCanonicalPath}
                result.append(data)

        return result