# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/invitation.py
# Compiled at: 2016-01-12 12:25:49
from .common import Permission
from .interface import APIObject
from .interface import readonly

@readonly('user', sync=False)
@readonly('id', sync=False)
@readonly('share_name')
@readonly('inviter')
@readonly('permissions')
class Invitation(APIObject):

    def __init__(self, api, email, sid=None):
        super(Invitation, self).__init__(api)
        from .user import User
        self._user = User(self.api, email)
        self._id = sid
        self._share_name = None
        self._inviter = None
        self._permissions = None
        return

    def from_json(self, json):
        self._id = json['share_id']
        self._share_name = json['share_name']
        from .user import User
        self._inviter = User(self.api, json['invited_by'])
        self._permissions = frozenset([ Permission(p) for p in json['permissions'] ])
        return self

    def load(self):
        data = self.api.get_invitation(self.user.email, self.id)
        self.from_json(data)

    def accept(self, external=False):
        self.api.accept_invitation(self.user.email, self.id, external=external)

    def delete(self):
        self.api.ignore_invitation(self.user.email, self.id)