# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sahriswiki/auth.py
# Compiled at: 2010-07-24 14:20:08
"""Authentication / Permissions

...
"""
import schema

class Permissions(object):

    def __init__(self, environ, username):
        super(Permissions, self).__init__()
        self.environ = environ
        self.username = username
        self._actions = []
        db = self.environ.dbm.session
        self._actions = [ permission.action for permission in db.query(schema.Permission).filter(schema.Permission.username == self.username)
                        ]

    def __contains__(self, action):
        return action in self._actions or 'SAHRIS_ADMIN' in self._actions

    def __repr__(self):
        return '<Permissions(%s %r)>' % (self.username, self._actions)