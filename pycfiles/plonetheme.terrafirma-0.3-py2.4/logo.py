# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/plonetheme/terrafirma/browser/logo.py
# Compiled at: 2008-05-03 14:27:58
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class LogoViewlet(ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('logo.pt')

    def update(self):
        super(LogoViewlet, self).update()
        self.navigation_root_url = self.portal_state.navigation_root_url()
        portal = self.portal_state.portal()
        logoName = portal.restrictedTraverse('base_properties').logoName
        self.logo_tag = portal.restrictedTraverse(logoName).tag()
        self.portal_title = self.portal_state.portal_title()