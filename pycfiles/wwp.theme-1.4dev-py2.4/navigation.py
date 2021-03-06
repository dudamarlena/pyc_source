# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/theme/portlets/navigation.py
# Compiled at: 2009-07-03 05:16:56
from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter, queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from plone.memoize.instance import memoize
from Acquisition import aq_inner, aq_base, aq_parent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INonStructuralFolder, IBrowserDefault
from Products.CMFPlone import utils
from Products.CMFPlone import PloneMessageFactory as _
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy

class INavigationPortlet(IPortletDataProvider):
    """A portlet which can render the navigation tree
    """
    __module__ = __name__
    name = schema.TextLine(title=_('label_navigation_title', default='Title'), description=_('help_navigation_title', default='The title of the navigation tree. Leave blank for the default, translated title.'), default='', required=False)
    root = schema.Choice(title=_('label_navigation_root_path', default='Root node'), description=_('help_navigation_root', default='You may search for and choose a folder to act as the root of the navigation tree. Leave blank to use the Plone site root.'), required=False, source=SearchableTextSourceBinder({'is_folderish': True}, default_query='path:'))
    includeTop = schema.Bool(title=_('label_include_top_node', default='Include top node'), description=_('help_include_top_node', default="Whether or not to show the top, or 'root', node in the navigation tree. This is affected by the 'Start level' setting."), default=False, required=False)
    currentFolderOnly = schema.Bool(title=_('label_current_folder_only', default='Only show the contents of the current folder.'), description=_('help_current_folder_only', default='If selected, the navigation tree will only show the current folder and its children at all times.'), default=False, required=False)
    topLevel = schema.Int(title=_('label_navigation_startlevel', default='Start level'), description=_('help_navigation_start_level', default='An integer value that specifies the number of folder levels below the site root that must be exceeded before the navigation tree will display. 0 means that the navigation tree should be displayed everywhere including pages in the root of the site. 1 means the tree only shows up inside folders located in the root and downwards, never showing at the top level.'), default=1, required=False)
    bottomLevel = schema.Int(title=_('label_navigation_tree_depth', default='Navigation tree depth'), description=_('help_navigation_tree_depth', default='How many folders should be included before the navigation tree stops. 0 means no limit. 1 only includes the root folder.'), default=0, required=False)


class Assignment(base.Assignment):
    __module__ = __name__
    implements(INavigationPortlet)
    title = _('Navigation')
    name = ''
    root = None
    currentFolderOnly = False
    includeTop = False
    topLevel = 1
    bottomLevel = 0

    def __init__(self, name='', root=None, currentFolderOnly=False, includeTop=False, topLevel=1, bottomLevel=0):
        self.name = name
        self.root = root
        self.currentFolderOnly = currentFolderOnly
        self.includeTop = includeTop
        self.topLevel = topLevel
        self.bottomLevel = bottomLevel


class Renderer(base.Renderer):
    __module__ = __name__

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.properties = getToolByName(context, 'portal_properties').navtree_properties
        self.urltool = getToolByName(context, 'portal_url')

    def title(self):
        return self.data.name or self.properties.name

    @property
    def available(self):
        tree = self.getNavTree()
        root = self.getNavRoot()
        return root is not None and len(tree['children']) > 0

    def include_top(self):
        return getattr(self.data, 'includeTop', self.properties.includeTop)

    def navigation_root(self):
        return self.getNavRoot()

    def root_type_name(self):
        root = self.getNavRoot()
        return queryUtility(IIDNormalizer).normalize(root.portal_type)

    def root_item_class(self):
        context = aq_inner(self.context)
        root = self.getNavRoot()
        if aq_base(root) is aq_base(context) or aq_base(root) is aq_base(aq_parent(aq_inner(context))) and utils.isDefaultPage(context, self.request, context):
            return 'navTreeCurrentItem'
        else:
            return ''

    def root_icon(self):
        ploneview = getMultiAdapter((self.context, self.request), name='plone')
        icon = ploneview.getIcon(self.getNavRoot())
        return icon.url

    def root_is_portal(self):
        root = self.getNavRoot()
        return aq_base(root) is aq_base(self.urltool.getPortalObject())

    def createNavTree(self):
        data = self.getNavTree()
        bottomLevel = self.data.bottomLevel or self.properties.getProperty('bottomLevel', 0)
        return self.recurse(children=data.get('children', []), level=1, bottomLevel=bottomLevel)

    @memoize
    def getNavRoot(self, _marker=[]):
        portal = self.urltool.getPortalObject()
        currentFolderOnly = self.data.currentFolderOnly or self.properties.getProperty('currentFolderOnlyInNavtree', False)
        topLevel = self.data.topLevel or self.properties.getProperty('topLevel', 0)
        rootPath = getRootPath(self.context, currentFolderOnly, topLevel, str(self.data.root))
        if rootPath == self.urltool.getPortalPath():
            return portal
        else:
            try:
                return portal.unrestrictedTraverse(rootPath)
            except (AttributeError, KeyError):
                return portal

    @memoize
    def getNavTree(self, _marker=[]):
        context = aq_inner(self.context)
        queryBuilder = getMultiAdapter((context, self.data), INavigationQueryBuilder)
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        return buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)

    def update(self):
        pass

    def render(self):
        return self._template()

    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('navigation_recurse.pt')


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(INavigationPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _('Add Navigation Portlet')
    description = _('This portlet display a navigation tree.')

    def create(self, data):
        return Assignment(name=data.get('name', ''), root=data.get('root', ''), currentFolderOnly=data.get('currentFolderOnly', False), includeTop=data.get('includeTop', False), topLevel=data.get('topLevel', 0), bottomLevel=data.get('bottomLevel', 0))


class EditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(INavigationPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _('Edit Navigation Portlet')
    description = _('This portlet display a navigation tree.')


class QueryBuilder(object):
    """Build a navtree query based on the settings in navtree_properties
    and those set on the portlet.
    """
    __module__ = __name__
    implements(INavigationQueryBuilder)
    adapts(Interface, INavigationPortlet)

    def __init__(self, context, portlet):
        self.context = context
        self.portlet = portlet
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        portal_url = getToolByName(context, 'portal_url')
        customQuery = getattr(context, 'getCustomNavQuery', None)
        if customQuery is not None:
            if utils.safe_callable(customQuery):
                query = customQuery()
            else:
                query = {}
            rootPath = getNavigationRoot(context, relativeRoot=portlet.root)
            currentPath = ('/').join(context.getPhysicalPath())
            query['path'] = currentPath.startswith(rootPath) or {'query': rootPath, 'depth': 1}
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


class NavtreeStrategy(SitemapNavtreeStrategy):
    """The navtree strategy used for the default navigation portlet
    """
    __module__ = __name__
    implements(INavtreeStrategy)
    adapts(Interface, INavigationPortlet)

    def __init__(self, context, portlet):
        SitemapNavtreeStrategy.__init__(self, context, portlet)
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        self.bottomLevel = portlet.bottomLevel or navtree_properties.getProperty('bottomLevel', 0)
        currentFolderOnly = portlet.currentFolderOnly or navtree_properties.getProperty('currentFolderOnlyInNavtree', False)
        topLevel = portlet.topLevel or navtree_properties.getProperty('topLevel', 0)
        self.rootPath = getRootPath(context, currentFolderOnly, topLevel, portlet.root)

    def subtreeFilter(self, node):
        sitemapDecision = SitemapNavtreeStrategy.subtreeFilter(self, node)
        if sitemapDecision == False:
            return False
        depth = node.get('depth', 0)
        if depth > 0 and self.bottomLevel > 0 and depth >= self.bottomLevel:
            return False
        else:
            return True


def getRootPath(context, currentFolderOnly, topLevel, root):
    """Helper function to calculate the real root path
    """
    context = aq_inner(context)
    if currentFolderOnly:
        folderish = getattr(aq_base(context), 'isPrincipiaFolderish', False) and not INonStructuralFolder.providedBy(context)
        parent = aq_parent(context)
        is_default_page = False
        browser_default = IBrowserDefault(parent, None)
        if browser_default is not None:
            is_default_page = browser_default.getDefaultPage() == context.getId()
        if not folderish or is_default_page:
            return ('/').join(parent.getPhysicalPath())
        else:
            return ('/').join(context.getPhysicalPath())
    rootPath = getNavigationRoot(context, relativeRoot=root)
    if topLevel > 0:
        contextPath = ('/').join(context.getPhysicalPath())
        if not contextPath.startswith(rootPath):
            return
        contextSubPathElements = contextPath[len(rootPath) + 1:]
        if contextSubPathElements:
            contextSubPathElements = contextSubPathElements.split('/')
            if len(contextSubPathElements) < topLevel:
                return
            rootPath = rootPath + '/' + ('/').join(contextSubPathElements[:topLevel])
        else:
            return
    return rootPath