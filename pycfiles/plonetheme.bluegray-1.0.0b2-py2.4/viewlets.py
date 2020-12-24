# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/bluegray/browser/viewlets.py
# Compiled at: 2008-10-10 20:44:03
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five import BrowserView
from zope.component import getMultiAdapter

class GlobalSectionsViewlet(ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/sections.pt')

    def update(self):
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        actions = context_state.actions()
        portal_tabs_view = getMultiAdapter((self.context, self.request), name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)
        selectedTabs = self.context.restrictedTraverse('selectedTabs')
        self.selected_tabs = selectedTabs('index_html', self.context, self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']


class SiteActionsViewlet(ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/site_actions.pt')

    def update(self):
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        self.site_actions = context_state.actions().get('site_actions', None)
        return