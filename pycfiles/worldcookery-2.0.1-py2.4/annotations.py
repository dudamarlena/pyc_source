# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/mail/annotations.py
# Compiled at: 2006-09-21 05:27:36
from persistent.list import PersistentList
from zope.interface import implements
from zope.event import notify
from zope.component import adapts
from zope.annotation.interfaces import IAnnotatable, IAnnotations
from zope.lifecycleevent import ObjectModifiedEvent, Attributes
from worldcookery.mail.interfaces import IMailSubscriptions
KEY = 'worldcookery.subscriptions'

class MailSubscriptionAnnotations(object):
    __module__ = __name__
    implements(IMailSubscriptions)
    adapts(IAnnotatable)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        emails = annotations.get(KEY)
        if emails is None:
            emails = annotations[KEY] = PersistentList()
        self.emails = emails
        return

    @property
    def subscribers(self):
        return tuple(self.emails)

    def subscribe(self, email):
        if email not in self.emails:
            self.emails.append(email)
            info = Attributes(IMailSubscriptions, 'subscribers')
            notify(ObjectModifiedEvent(self.context, info))

    def unsubscribe(self, email):
        if email in self.emails:
            self.emails.remove(email)
            info = Attributes(IMailSubscriptions, 'subscribers')
            notify(ObjectModifiedEvent(self.context, info))