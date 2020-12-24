# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plonetheme/cultureCab/browser/sections.py
# Compiled at: 2010-09-22 06:02:53
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class GlobalSectionsViewlet(ViewletBase):
    index = ViewPageTemplateFile('sections.pt')

    def update(self):
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        actions = context_state.actions()
        portal_tabs_view = getMultiAdapter((self.context, self.request), name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs()
        selectedTabs = self.context.restrictedTraverse('selectedTabs')
        self.selected_tabs = selectedTabs('index_html', self.context, self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']