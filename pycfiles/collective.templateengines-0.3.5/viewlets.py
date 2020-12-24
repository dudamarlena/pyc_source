# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/thet-data/data/dev/htu/bda.htu.buildout/src/collective.teaser/collective/teaser/browser/viewlets.py
# Compiled at: 2013-03-13 08:34:51
from zope.component import getMultiAdapter
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName

class TeaserPortletsViewlet(ViewletBase):
    name = 'Teaser portlets'
    manage_view = '@@manage-teaserportlets'

    @property
    def display(self):
        return True

    def update(self):
        if not self.display:
            self.canManagePortlets = False
            return
        context_state = getMultiAdapter((
         self.context, self.request), name='plone_context_state')
        self.manageUrl = '%s/%s' % (context_state.view_url(), self.manage_view)
        mt = getToolByName(self.context, 'portal_membership')
        self.canManagePortlets = mt.checkPermission('Portlets: Manage portlets', self.context)