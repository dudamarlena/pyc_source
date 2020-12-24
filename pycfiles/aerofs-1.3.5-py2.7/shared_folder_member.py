# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/shared_folder_member.py
# Compiled at: 2016-03-28 13:15:32
from .common import Permission
from .interface import APIObject
from .interface import enable_etags
from .interface import readonly
from .interface import synced

@readonly('shared_folder', sync=False)
@readonly('email', sync=False)
@readonly('first_name')
@readonly('last_name')
@synced('permissions')
class SFMember(APIObject):

    def __init__(self, api, sid, email=None):
        super(SFMember, self).__init__(api)
        from .shared_folder import SharedFolder
        self._shared_folder = SharedFolder(self.api, sid)
        self._email = email
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
        self._first_name = json['first_name']
        self._last_name = json['last_name']
        self._permissions = frozenset([ Permission(p) for p in json['permissions'] ])
        return self

    @enable_etags
    def load(self):
        data = self.api.get_sf_member(self.shared_folder.id, self.email)
        self.from_json(data)

    @enable_etags
    def save_permissions(self, matching=False):
        if not matching:
            self._etags = None
        data = self.api.update_sf_member(self.shared_folder.id, self.email, self._permissions, ifmatch=self._etags)
        self.from_json(data)
        return

    def create(self, email, permissions):
        data = self.api.add_sf_member(self.shared_folder.id, email, permissions)
        self.from_json(data)

    @enable_etags
    def delete(self, matching=False):
        if not matching:
            self._etags = None
        self.api.remove_sf_member(self.shared_folder.id, self.email, ifmatch=self._etags)
        return