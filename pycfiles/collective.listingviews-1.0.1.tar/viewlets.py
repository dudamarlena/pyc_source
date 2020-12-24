# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/linkedin/browser/viewlets.py
# Compiled at: 2010-02-02 18:40:16
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase, SiteActionsViewlet
from collective.linkedin.browser.config import ld_action_id
from collective.linkedin.browser.company_info import CompanyInfo

class CustomSiteActionsViewlet(SiteActionsViewlet, CompanyInfo):
    __module__ = __name__
    index = ViewPageTemplateFile('templates/site_actions.pt')

    def render(self):
        return self.index()

    def action_visible(self):
        settings = self.get_settings()
        return settings and settings.action_popup or None

    def show_popup(self):
        return self.company_name() and self.action_visible()

    def linkedin_action_id(self):
        return ld_action_id