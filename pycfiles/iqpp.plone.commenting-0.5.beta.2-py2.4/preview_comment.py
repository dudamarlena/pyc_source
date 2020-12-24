# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/browser/preview_comment.py
# Compiled at: 2007-10-06 06:19:54
from datetime import datetime
from pytz import UTC
from zope.interface import Interface
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('iqpp.plone.commenting')
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from iqpp.plone.commenting.interfaces import ICommentTransformations
from iqpp.plone.commenting.content import Comment
from iqpp.plone.commenting import utils

class PreviewCommentView(BrowserView):
    """A view to preview a comment before it is added / edited.
    """
    __module__ = __name__

    def getData(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.isAnonymousUser() == True:
            member_id = ''
            name = self.request.get('name')
            email = self.request.get('email')
        else:
            member_id = mtool.getAuthenticatedMember().getId()
            name = ''
            email = ''
        temp_comment = Comment(id='', reply_to='', subject='', message=self.request.get('message'))
        t = ICommentTransformations(temp_comment)
        t.transformMessage()
        member_info = utils.getMemberInfo(self.context, member_id, name, email)
        tool = getToolByName(self.context, 'translation_service')
        created = tool.ulocalized_time(datetime.now(UTC).isoformat(), long_format=True)
        return {'name': member_info['name'], 'email': member_info['email'], 'subject': self.request.get('subject'), 'transformed_message': temp_comment.transformed_message, 'message': temp_comment.message, 'created': created}

    def showAddButton(self):
        """Returns True if user adds a comment.
        """
        if self.request.get('action') == 'add':
            return True
        else:
            return False

    def showEditButton(self):
        """Returns True if user edits a comment.
        """
        return not self.showAddButton()