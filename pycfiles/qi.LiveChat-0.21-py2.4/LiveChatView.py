# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/LiveChat/browser/LiveChatView.py
# Compiled at: 2008-07-25 11:17:39
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from qi.LiveChat.browser.ILiveChatView import ILiveChatView

class LiveChatView(BrowserView):
    """
        """
    __module__ = __name__
    implements(ILiveChatView)
    __call__ = ViewPageTemplateFile('livechat_view.pt')

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.mt = getToolByName(context, 'portal_membership')

    def getUser(self):
        """
                """
        return self.mt.getAuthenticatedMember()

    def isAnonymous(self):
        """
                """
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        if portal_state.anonymous():
            return True
        return False