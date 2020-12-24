# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/browser/delete_comments.py
# Compiled at: 2007-10-06 06:19:54
from DateTime import DateTime
from zope.interface import implements
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('iqpp.plone.commenting')
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from iqpp.plone.commenting import utils
from iqpp.plone.commenting.config import MESSAGES
from iqpp.plone.commenting.interfaces import ICommenting
from iqpp.plone.commenting.interfaces import ICommentingOptions

class DeleteCommentsView(BrowserView):
    """Provides Methods to delete comments.
    """
    __module__ = __name__

    def deleteComment(self):
        """Deletes a comment with given comment_id (via request) of context.
        """
        ptool = getToolByName(self.context, 'plone_utils')
        comment_id = self.request.get('comment_id')
        manager = ICommenting(self.context)
        result = manager.deleteComment(comment_id)
        if result == True:
            ptool.addPortalMessage(_(MESSAGES['comment-deleted']))
        else:
            ptool.addPortalMessage(_(MESSAGES['comment-not-deleted']))
        self._redirect()

    def deleteComments(self):
        """Deletes all comments of context.
        """
        manager = ICommenting(self.context)
        manager.deleteComments()
        utils = getToolByName(self.context, 'plone_utils')
        utils.addPortalMessage(_(MESSAGES['comments-deleted']))
        self._redirect()

    def _redirect(self):
        """
        """
        url = self.context.absolute_url()
        b_start = self.request.get('b_start', None)
        if b_start is not None:
            url = '%s?b_start:int=%d' % (url, b_start)
        self.request.response.redirect(url)
        return