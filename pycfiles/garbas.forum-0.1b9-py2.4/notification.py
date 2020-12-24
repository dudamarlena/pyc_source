# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/garbas/forum/notification.py
# Compiled at: 2008-09-27 01:25:51
from Acquisition import aq_inner
from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList
from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.utils import getToolByName
from garbas.forum.interfaces import IForumNotification
NOTIFICATION_KEY = 'garbas.forum.notification'

class ForumNotification(object):
    """ notification """
    __module__ = __name__
    implements(IForumNotification)

    def __init__(self, context):
        self.context = aq_inner(context)
        self.annotations = IAnnotations(self.context)
        notifications = self.annotations.get(NOTIFICATION_KEY, None)
        if notifications is None:
            self.annotations[NOTIFICATION_KEY] = PersistentList()
        return

    def email_list(self, ignore=[]):
        email_list = []
        membership = getToolByName(self.context, 'portal_membership')
        for email in self.annotations[NOTIFICATION_KEY]:
            if email not in ignore:
                try:
                    ploneMember = membership.getMemberById(email)
                except:
                    ploneMember = None
                else:
                    if ploneMember:
                        ploneMemberEmail = ploneMember.getProperty('email')
                        if ploneMemberEmail:
                            email = ploneMemberEmail
                    email_list.append(email)

        return email_list

    def subscribe(self, email):
        if email not in self.annotations[NOTIFICATION_KEY]:
            if email:
                self.annotations[NOTIFICATION_KEY].append(email)

    def unsubscribe(self, email):
        if email in self.annotations[NOTIFICATION_KEY]:
            self.annotations[NOTIFICATION_KEY].remove(email)