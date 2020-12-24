# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/Andreas09Theme/browser/viewlets.py
# Compiled at: 2008-09-09 18:26:37
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class PortalTitleViewlet(ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('portal_title_viewlet.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        self.portal_title = self.portal_state.portal_title
        self.portal_description = self.portal_state.portal().Description()