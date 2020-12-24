# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jack/src/dis-git/igor/test/fixtures/testIgor/plugins/user/igorplugin.py
# Compiled at: 2019-02-04 04:52:11
from __future__ import print_function
from __future__ import unicode_literals
from builtins import object
import os, sys, re
NAME_RE = re.compile(b'[a-zA-Z_][-a-zA-Z0-9_.]+')
DEBUG = False

class UserPlugin(object):

    def __init__(self, igor):
        self.igor = igor

    def index(self, token=None, callerToken=None):
        raise self.igor.app.raiseNotfound()

    def add(self, token=None, callerToken=None, username=None, password=None, returnTo=None):
        if not NAME_RE.match(username):
            self.igor.app.raiseHTTPError(b'400 Illegal name for user')
        if self.igor.databaseAccessor.get_key(b'identities/%s' % username, b'application/x-python-object', b'multi', callerToken):
            self.igor.app.raiseHTTPError(b'400 user already exists')
        self.igor.databaseAccessor.put_key(b'identities/%s' % username, b'text/plain', b'ref', b'', b'text/plain', callerToken, replace=True)
        self.igor.databaseAccessor.put_key(b'people/%s' % username, b'text/plain', b'ref', b'', b'text/plain', callerToken, replace=True)
        self.igor.internal.accessControl(b'setUserPassword', token=callerToken, username=username, password=password)
        if self.igor.internal.accessControl(b'hasCapabilitySupport'):
            self.igor.internal.accessControl(b'newToken', token=callerToken, tokenId=b'admin-data', newOwner=b'identities/%s' % username, newPath=b'/data/identities/%s' % username, get=b'descendant-or-self', put=b'descendant', post=b'descendant', delete=b'descendant', delegate=True)
            self.igor.internal.accessControl(b'newToken', token=callerToken, tokenId=b'admin-data', newOwner=b'identities/%s' % username, newPath=b'/data/people/%s' % username, put=b'descendant', post=b'descendant', delete=b'descendant', delegate=True)
        self.igor.internal.save(token)
        if returnTo:
            return self.igor.app.raiseSeeother(returnTo)
        return b''

    def delete(self, token=None, callerToken=None, username=None, returnTo=None):
        if not NAME_RE.match(username):
            self.igor.app.raiseHTTPError(b'400 Illegal name for user')
        if not self.igor.databaseAccessor.get_key(b'identities/%s' % username, b'application/x-python-object', b'multi', callerToken):
            self.igor.app.raiseHTTPError(b'404 user %s does not exist' % username)
        self.igor.databaseAccessor.delete_key(b'people/%s' % username, callerToken)
        self.igor.databaseAccessor.delete_key(b'identities/%s' % username, callerToken)
        self.igor.internal.save(token)
        if returnTo:
            return self.igor.app.raiseSeeother(returnTo)
        return b''

    def password(self, token=None, callerToken=None, username=None, password=None, returnTo=None):
        if not NAME_RE.match(username):
            self.igor.app.raiseHTTPError(b'400 Illegal name for user')
        if not self.igor.databaseAccessor.get_key(b'identities/%s' % username, b'application/x-python-object', b'multi', callerToken):
            self.igor.app.raiseHTTPError(b'404 user %s does not exist' % username)
        self.igor.internal.accessControl(b'setUserPassword', token=callerToken, username=username, password=password)
        self.igor.internal.save(token)
        if returnTo:
            return self.igor.app.raiseSeeother(returnTo)
        return b''


def igorPlugin(igor, pluginName, pluginData):
    return UserPlugin(igor)