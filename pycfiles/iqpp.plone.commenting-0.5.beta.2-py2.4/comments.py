# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/viewlets/comments.py
# Compiled at: 2007-10-06 06:19:54
from datetime import datetime
from datetime import timedelta
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from iqpp.plone.commenting import utils
from iqpp.plone.commenting.interfaces import ICommenting
from iqpp.plone.commenting.interfaces import ICommentingOptions
from iqpp.plone.commenting.viewlets.base import CommentingViewletsBase

class CommentsViewlet(ViewletBase, CommentingViewletsBase):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('comments.pt')

    def __init__(self, context, request, view, manager):
        """
        """
        super(CommentsViewlet, self).__init__(context, request, view, manager)
        self.mtool = getToolByName(context, 'portal_membership')

    def getComments(self, id=''):
        """Returns all comments of context.
        """
        if id is None:
            id = ''
            reverse = True
        else:
            reverse = False
        mtool = getToolByName(self.context, 'portal_membership')
        auth_member_id = mtool.getAuthenticatedMember().getId()
        comments = ICommenting(self.context).getComments(id, reverse=reverse)
        result = []
        i = 0
        for comment in comments:
            if comment.review_state == 'published' or comment.member_id and comment.member_id == auth_member_id or self.mtool.checkPermission('Manage comments', self.context) == True:
                member_info = utils.getMemberInfo(self.context, comment.member_id, comment.name, comment.email)
                if i % 2 == 0:
                    klass = 'comment even'
                else:
                    klass = 'comment odd'
                i += 1
                if member_info['is_manager'] == True:
                    klass = klass + ' manager'
                tool = getToolByName(self.context, 'translation_service')
                created_local = tool.ulocalized_time(comment.created.isoformat(), long_format=True)
                result.append({'id': comment.id, 'subject': comment.subject, 'message': comment.message, 'transformed_message': comment.transformed_message, 'name': member_info['name'], 'email': member_info['email'], 'class': klass, 'review_state': comment.review_state, 'created': comment.created, 'created_local': created_local, 'member_id': comment.member_id, 'show_delete_button': self._showDeleteButton(), 'show_edit_button': self._showEditButton(comment), 'show_manage_button': self._showManageButton(), 'show_publish_button': self._showPublishButton(comment), 'show_reject_button': self._showRejectButton(comment), 'show_reply_button': self._showReplyButton(comment)})

        return result

    def _showEditButton(self, comment):
        """Returns True when the user is allowed to edit given comment.
        """
        options = ICommentingOptions(self.context)
        edit_own_comments = options.getEffectiveOption('edit_own_comments')
        if self._showManageButton() == True:
            return False
        if comment.member_id is not None and comment.member_id == self.mtool.getAuthenticatedMember().getId() and comment.review_state in edit_own_comments:
            return True
        else:
            return False
        return

    def _showDeleteButton(self):
        """Returns True if the authenticated user is allowed to delete a 
        comment.
        """
        if self.mtool.checkPermission('Delete comments', self.context) == True:
            return True
        return False

    def _showManageButton(self):
        """Returns True if the authenticated user is allowed to manage a 
        comment.
        """
        if self.mtool.checkPermission('Manage comments', self.context) == True:
            return True
        else:
            return False

    def _showPublishButton(self, comment):
        """Returns True if the comment is able and allowed to be published.
        """
        if self.mtool.checkPermission('Review comments', self.context) == True and comment.review_state != 'published':
            return True
        else:
            return False

    def _showRejectButton(self, comment):
        """Returns True if the comment is able and allowed to be rejected.
        """
        if self.mtool.checkPermission('Review comments', self.context) == True and comment.review_state != 'private':
            return True
        else:
            return False

    def _showReplyButton(self, comment):
        """Returns True if the authenticated user is allowed to reply to 
        context.
        """
        if comment.reply_to is None:
            if self.mtool.checkPermission('Reply to item', self.context) == True:
                return True
        elif self.mtool.checkPermission('Reply to comment', self.context) == True:
            return True
        return False