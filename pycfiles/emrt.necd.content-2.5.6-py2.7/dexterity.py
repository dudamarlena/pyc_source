# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/subscriptions/dexterity.py
# Compiled at: 2019-02-15 13:51:23
from zope.annotation.interfaces import IAnnotations
from BTrees.OOBTree import OOBTree
UNSUBSCRIPTION_KEY = 'emrt.necd.content.subscriptions.unsubscribed'

class NotificationUnsubscriptions(object):

    def __init__(self, context):
        self.context = context

    def get(self):
        annotated = IAnnotations(self.context)
        return annotated.get(UNSUBSCRIPTION_KEY, OOBTree())

    def get_user_data(self, userid):
        return self.get().get(userid, OOBTree())

    def unsubscribe(self, userid, notifications={}, roles=[]):
        """
        Save the unsubscribed notifications dict.
        The key of the dict should be the role name, and the value
         the list of notifications that will be unsubscribed:

         {
            ROLE_CP: ['conclusion_to_comment'],
         }
        """
        annotated = IAnnotations(self.context)
        data = annotated.get(UNSUBSCRIPTION_KEY, OOBTree())
        if notifications:
            data[userid] = notifications
        else:
            del data[userid]
        annotated[UNSUBSCRIPTION_KEY] = data
        return 1