# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/browser/review_comments.py
# Compiled at: 2007-10-06 06:19:54
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('iqpp.plone.commenting')
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from iqpp.plone.commenting.config import MESSAGES
from iqpp.plone.commenting.interfaces import ICommenting

class ReviewCommentsView(BrowserView):
    """Provides methods to review comments.
    """
    __module__ = __name__

    def publishComment(self):
        """
        """
        ptool = getToolByName(self.context, 'plone_utils')
        comment_id = self.request.get('comment_id')
        commenting = ICommenting(self.context)
        result = commenting.publishComment(comment_id)
        if result:
            ptool.addPortalMessage(_(MESSAGES['comment-published']))
        else:
            ptool.addPortalMessage(_(MESSAGES['comment-not-published']))
        self._redirect()

    def rejectComment(self):
        """
        """
        ptool = getToolByName(self.context, 'plone_utils')
        comment_id = self.request.get('comment_id')
        commenting = ICommenting(self.context)
        result = commenting.rejectComment(comment_id)
        if result:
            ptool.addPortalMessage(_(MESSAGES['comment-rejected']))
        else:
            ptool.addPortalMessage(_(MESSAGES['comment-not-rejected']))
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