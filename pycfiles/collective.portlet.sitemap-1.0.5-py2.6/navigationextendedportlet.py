# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/portlet/sitemap/navigationextendedportlet.py
# Compiled at: 2012-10-15 04:02:25
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts, getMultiAdapter
from plone.memoize.instance import memoize
from plone.app.portlets.portlets import navigation
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.navigation.navtree import buildFolderTree
from zope import schema
from zope.formlib import form
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import utils
from collective.portlet.sitemap import NavigationExtendedPortletMessageFactory as _

class INavigationExtendedPortlet(navigation.INavigationPortlet):
    """A portlet

    It inherits from INavigationPortlet
    """
    displayAsSiteMap = schema.Bool(title=_('label_display_as_site_map', default='Display as Site Map'), description=_('help_display_as_site_map', default='If checked display all folders as a site map'), default=True, required=False)
    siteMapDepth = schema.Int(title=_('label_site_map_depth', default='Site map depth'), description=_('help_site_map_depth', default='If previous field is checked set the site map depth'), default=2, required=False)


class Assignment(navigation.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(INavigationExtendedPortlet)
    title = _('Navigation Extended')
    name = ''
    root = None
    currentFolderOnly = False
    includeTop = False
    topLevel = 0
    bottomLevel = 0
    displayAsSiteMap = True
    siteMapDepth = 2

    def __init__(self, name='', root=None, currentFolderOnly=False, includeTop=False, topLevel=0, bottomLevel=0, displayAsSiteMap=True, siteMapDepth=2):
        self.name = name
        self.root = root
        self.currentFolderOnly = currentFolderOnly
        self.includeTop = includeTop
        self.topLevel = topLevel
        self.bottomLevel = bottomLevel
        self.displayAsSiteMap = displayAsSiteMap
        self.siteMapDepth = siteMapDepth


class Renderer(navigation.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    @memoize
    def getNavTree(self, _marker=[]):
        context = aq_inner(self.context)
        queryBuilder = getMultiAdapter((context, self.data), INavigationExtendedQueryBuilder)
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)

    recurse = ViewPageTemplateFile('navigation_extended_recurse.pt')


class AddForm(navigation.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(INavigationExtendedPortlet)

    def create(self, data):
        return Assignment(name=data.get('name', ''), root=data.get('root', ''), currentFolderOnly=data.get('currentFolderOnly', False), includeTop=data.get('includeTop', False), topLevel=data.get('topLevel', 0), bottomLevel=data.get('bottomLevel', 0), displayAsSiteMap=data.get('displayAsSiteMap', True), siteMapDepth=data.get('siteMapDepth', 2))


class EditForm(navigation.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(INavigationExtendedPortlet)


class INavigationExtendedQueryBuilder(INavigationQueryBuilder):
    """An object which returns a catalog query when called, used to 
    construct a navigation tree.
    """

    def __call__():
        """Returns a mapping describing a catalog query used to build a
           navigation structure.
        """
        pass


class NavigationExtendedQueryBuilder(object):
    """Build a navtree query based on the settings in navtree_properties
    and those set on the portlet.
    """
    implements(INavigationExtendedQueryBuilder)
    adapts(Interface, INavigationExtendedPortlet)

    def __init__(self, context, portlet):
        self.context = context
        self.portlet = portlet
        portal_properties = utils.getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        portal_url = utils.getToolByName(context, 'portal_url')
        customQuery = getattr(context, 'getCustomNavQuery', None)
        if customQuery is not None and utils.safe_callable(customQuery):
            query = customQuery()
        else:
            query = {}
        rootPath = getNavigationRoot(context, relativeRoot=portlet.root)
        currentPath = ('/').join(context.getPhysicalPath())
        if portlet.displayAsSiteMap:
            query['path'] = {'query': rootPath, 'depth': portlet.siteMapDepth}
        elif not currentPath.startswith(rootPath):
            query['path'] = {'query': rootPath, 'depth': 1}
        else:
            query['path'] = {'query': currentPath, 'navtree': 1}
        topLevel = portlet.topLevel or navtree_properties.getProperty('topLevel', 0)
        if topLevel and topLevel > 0:
            query['path']['navtree_start'] = topLevel + 1
        query['portal_type'] = utils.typesToList(context)
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder
        if navtree_properties.getProperty('enable_wf_state_filtering', False):
            query['review_state'] = navtree_properties.getProperty('wf_states_to_show', ())
        self.query = query
        return

    def __call__(self):
        return self.query