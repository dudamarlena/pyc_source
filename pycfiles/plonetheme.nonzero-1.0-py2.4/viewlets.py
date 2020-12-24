# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/nonzero/browser/viewlets.py
# Compiled at: 2008-05-16 18:52:05
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter

class NonzeroLogoViewlet(ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('nonzero_logo.pt')

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        portal = portal_state.portal()
        self.portal = portal.absolute_url()
        self.portal_title = portal_state.portal_title()
        self.portal_desc = portal.description