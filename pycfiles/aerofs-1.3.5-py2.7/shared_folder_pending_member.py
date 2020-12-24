# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/shared_folder_pending_member.py
# Compiled at: 2016-03-28 13:15:32
from .common import Permission
from .interface import APIObject
from .interface import readonly

@readonly('shared_folder', sync=False)
@readonly('id', sync=False)
@readonly('first_name')
@readonly('last_name')
@readonly('permissions')
class SFPendingMember(APIObject):

    def __init__(self, api, sid, email=None):
        super(SFPendingMember, self).__init__(api)
        from .shared_folder import SharedFolder
        self._shared_folder = SharedFolder(self.api, sid)
        self._email = email
        self._inviter = None
        self._first_name = None
        self._last_name = None
        self._permissions = None
        return

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.shared_folder.id == other.shared_folder.id and self.email == other.email
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.shared_folder.id != other.shared_folder.id and self.email != other.email
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def from_json(self, json):
        self._email = json['email']
        self._first_name = json.get('first_name')
        self._last_name = json.get('last_name')
        self._inviter = json['invited_by']
        self._permissions = frozenset([ Permission(p) for p in json['permissions'] ])
        return self

    def load(self):
        data = self.api.get_sf_pending_member(self.shared_folder.id, self.email)
        self.from_json(data)

    def create(self, email, permissions, note):
        data = self.api.add_sf_pending_member(self.shared_folder.id, email, permissions, note)
        self.from_json(data)

    def delete(self):
        self.api.remove_sf_pending_member(self.shared_folder.id, self.email)