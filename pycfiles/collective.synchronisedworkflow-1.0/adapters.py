# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/sylvester/browser/adapters.py
# Compiled at: 2009-07-09 17:23:46
from zope.interface import implements
from interfaces import ITwitterCredentialsProvider

class MemberDataTwitterCredentialsProvider:
    __module__ = __name__
    implements(ITwitterCredentialsProvider)

    def __init__(self, context):
        self.context = context

    def username(self):
        return self.context.getProperty('twitterUsername')

    def password(self):
        return self.context.getProperty('twitterPassword')


class ReMemberTwitterCredentialsProvider:
    __module__ = __name__
    implements(ITwitterCredentialsProvider)

    def __init__(self, context):
        self.context = context

    def username(self):
        return self.context.Schema().getField('twitterUsername').getAccessor(self.context)()

    def password(self):
        return self.context.Schema().getField('twitterPassword').getAccessor(self.context)()