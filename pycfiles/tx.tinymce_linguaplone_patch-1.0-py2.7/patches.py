# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tx/tinymce_linguaplone_patch/patches.py
# Compiled at: 2013-08-20 10:28:33
from zope.interface import implements
from zope.component import getUtility
try:
    import json
except:
    import simplejson as json

from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

def getListing(self, filter_portal_types, rooted, document_base_url, upload_type=None):
    """Returns the actual listing"""
    catalog_results = []
    results = {}
    object = aq_inner(self.context)
    portal_catalog = getToolByName(object, 'portal_catalog')
    normalizer = getUtility(IIDNormalizer)
    if not IFolderish.providedBy(object):
        object = object.getParentNode()
    if rooted == 'True' and document_base_url[:-1] == object.absolute_url():
        results['parent_url'] = ''
    else:
        results['parent_url'] = object.getParentNode().absolute_url()
    if rooted == 'True':
        results['path'] = self.getBreadcrumbs(results['parent_url'])
    else:
        results['path'] = self.getBreadcrumbs()
    path = ('/').join(object.getPhysicalPath())
    for brain in portal_catalog(portal_type=filter_portal_types, sort_on='getObjPositionInParent', path={'query': path, 'depth': 1}):
        catalog_results.append({'id': brain.getId, 
           'uid': brain.UID, 
           'url': brain.getURL(), 
           'portal_type': brain.portal_type, 
           'normalized_type': normalizer.normalize(brain.portal_type), 
           'title': brain.Title == '' and brain.id or brain.Title, 
           'icon': brain.getIcon, 
           'is_folderish': brain.is_folderish})

    results['items'] = catalog_results
    results['upload_allowed'] = False
    if upload_type:
        portal_types = getToolByName(object, 'portal_types')
        fti = getattr(portal_types, upload_type, None)
        if fti is not None:
            results['upload_allowed'] = fti.isConstructionAllowed(object)
    return json.dumps(results)


from zope.component import getMultiAdapter

def breadcrumbs(self, startup_directory=None):
    if not self._updated:
        raise AssertionError
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name='plone_portal_state')
        bc_view = context.restrictedTraverse('@@breadcrumbs_view')
        crumbs = bc_view.breadcrumbs()
        newcrumbs = self.widget.restrict_browsing_to_startup_directory or [
         {'Title': 'Home', 'absolute_url': self.genRefBrowserUrl(portal_state.portal_url())}]
        if portal_state.portal_url() != portal_state.navigation_root_url():
            nav_root_path = portal_state.navigation_root_path()
            nav_root = self.context.restrictedTraverse(nav_root_path)
            newcrumbs.append({'Title': nav_root.Title(), 'absolute_url': self.genRefBrowserUrl(portal_state.navigation_root_url())})
    else:
        startup_dir_url = startup_directory or utils.getStartupDirectory(context, self.widget.getStartupDirectory(context, self.field))
        newcrumbs = []
        crumbs = [ c for c in crumbs if c['absolute_url'].startswith(startup_dir_url)
                 ]
    for c in crumbs:
        c['absolute_url'] = self.genRefBrowserUrl(c['absolute_url'])
        newcrumbs.append(c)

    return newcrumbs


from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder

def SitemapQueryBuilder__init__(self, context):
    NavtreeQueryBuilder.__init__(self, context)
    portal_url = getToolByName(context, 'portal_url')
    portal_properties = getToolByName(context, 'portal_properties')
    navtree_properties = getattr(portal_properties, 'navtree_properties')
    sitemapDepth = navtree_properties.getProperty('sitemapDepth', 2)
    if context.REQUEST.get('sitemap_for_current_context', False):
        self.query['path'] = {'query': ('/').join(context.getPhysicalPath()), 'depth': sitemapDepth}
    else:
        self.query['path'] = {'query': portal_url.getPortalPath(), 'depth': sitemapDepth}


import json

def getSearchResults(self, filter_portal_types, searchtext):
    """Returns the actual search result"""
    catalog_results = []
    results = {}
    results['parent_url'] = ''
    results['path'] = []
    if searchtext:
        for brain in self.context.portal_catalog.searchResults({'SearchableText': '%s*' % searchtext, 'portal_type': filter_portal_types, 'sort_on': 'sortable_title'}):
            catalog_results.append({'id': brain.getId, 
               'uid': brain.UID, 
               'url': brain.getURL(), 
               'portal_type': brain.portal_type, 
               'title': brain.Title == '' and brain.id or brain.Title, 
               'icon': brain.getIcon, 
               'is_folderish': brain.is_folderish})

    results['items'] = catalog_results
    results['upload_allowed'] = False
    return json.dumps(results)