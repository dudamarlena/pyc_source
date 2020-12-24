# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/webcouturier/icompany/theme/browser/viewlets.py
# Compiled at: 2008-04-30 11:18:20
from zope.component import getMultiAdapter
from zope.interface import implements
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from plone.app.portlets.portlets.navigation import Assignment
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from interfaces import ISubmenuViewlet

class SearchBoxViewlet(common.SearchBoxViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/webcouturier_searchbox.pt')


class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    __module__ = __name__
    implements(ISubmenuViewlet)
    render = ViewPageTemplateFile('templates/webcouturier_sections.pt')
    sublevel = ViewPageTemplateFile('templates/webcouturier_subsections.pt')

    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        self.portal = self.portal_state.portal()
        self.properties = getToolByName(self.context, 'portal_properties').navtree_properties
        self.data = Assignment()

    def getSubmenu(self, selected_id=''):
        if selected_id != '':
            tabObj = getattr(self.portal, selected_id)
            strategy = getMultiAdapter((tabObj, self.data), INavtreeStrategy)
            queryBuilder = NavtreeQueryBuilder(tabObj)
            query = queryBuilder()
            query['depth'] = 1
            data = buildFolderTree(tabObj, obj=self.context, query=query, strategy=strategy)
            bottomLevel = 1
            return self.sublevel(children=data.get('children', []), level=1, bottomLevel=bottomLevel).strip()