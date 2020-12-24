# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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