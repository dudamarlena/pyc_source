# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/viewlets/add_comment_button.py
# Compiled at: 2007-10-06 06:19:54
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from iqpp.plone.commenting.viewlets.base import CommentingViewletsBase

class AddCommentButtonViewlet(ViewletBase, CommentingViewletsBase):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('add_comment_button.pt')

    def showAddButton(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.checkPermission('Reply to item', self.context)