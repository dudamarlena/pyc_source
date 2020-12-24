# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/browser/my_comments.py
# Compiled at: 2007-10-06 06:19:54
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from iqpp.plone.commenting import utils
from iqpp.plone.commenting.interfaces import IGlobalCommenting

class MyCommentsView(BrowserView):
    """
    """
    __module__ = __name__

    def getCommentsForMember(self, member_id=None):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        cm = IGlobalCommenting(self.context)
        comments = cm.getCommentsForMember(member_id)
        result = []
        for (i, comment) in enumerate(comments):
            if mtool.checkPermission('Manage portal', self.context) is None and comment.review_state != 'published':
                continue
            if i % 2 == 0:
                css_class = 'even'
            else:
                css_class = 'odd'
            member_info = utils.getMemberInfo(self.context, comment.member_id, comment.name, comment.email)
            result.append({'id': comment.id, 'subject': comment.subject, 'message': comment.message, 'transformed_message': comment.transformed_message, 'name': member_info['name'], 'email': member_info['email'], 'css_class': css_class, 'review_state': comment.review_state, 'created': comment.created, 'member_id': comment.member_id})

        return result