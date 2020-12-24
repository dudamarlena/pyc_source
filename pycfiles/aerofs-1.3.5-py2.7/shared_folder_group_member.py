# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/shared_folder_group_member.py
# Compiled at: 2016-01-12 12:25:49
from .common import Permission
from .interface import APIObject
from .interface import readonly
from .interface import synced

@readonly('shared_folder', sync=False)
@readonly('id', sync=False)
@readonly('name')
@synced('permissions')
class SFGroupMember(APIObject):

    def __init__(self, api, sid, gid=None):
        super(SFGroupMember, self).__init__(api)
        from .shared_folder import SharedFolder
        self._shared_folder = SharedFolder(self.api, sid)
        self._id = gid
        self._name = None
        self._permissions = None
        return

    def from_json(self, json):
        self._id = json['id']
        self._name = json['name']
        self._permissions = frozenset([ Permission(p) for p in json['permissions'] ])
        return self

    def load(self):
        data = self.api.get_sf_group_member(self.shared_folder.id, self.id)
        self.from_json(data)

    def save_permissions(self):
        data = self.api.update_sf_group_member(self.shared_folder.id, self.id, self._permissions)
        self.from_json(data)

    def create(self, gid, permissions):
        data = self.api.add_sf_group_member(self.shared_folder.id, gid, permissions)
        self.from_json(data)

    def delete(self):
        self.api.remove_sf_group_member(self.shared_folder.id, self.id)