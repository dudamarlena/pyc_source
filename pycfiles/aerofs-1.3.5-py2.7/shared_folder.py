# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/shared_folder.py
# Compiled at: 2016-01-12 12:25:49
from .common import Permission
from .interface import APIObject
from .interface import readonly

@readonly('id', sync=False)
@readonly('name')
@readonly('is_external')
@readonly('members')
@readonly('groups')
@readonly('pending')
@readonly('caller_permissions')
class SharedFolder(APIObject):

    def __init__(self, api, sid=None):
        super(SharedFolder, self).__init__(api)
        self._id = sid
        self._name = None
        self._is_external = None
        self._members = None
        self._groups = None
        self._pending = None
        self._caller_permissions = None
        return

    def from_json(self, json):
        self._id = json['id']
        self._name = json['name']
        self._is_external = json['is_external']
        from .shared_folder_member import SFMember
        self._members = frozenset([ SFMember(self.api, self.id).from_json(f) for f in json['members']
                                  ])
        from .shared_folder_group_member import SFGroupMember
        self._groups = frozenset([ SFGroupMember(self.api, self.id).from_json(f) for f in json['groups']
                                 ])
        from .shared_folder_pending_member import SFPendingMember
        self._pending = frozenset([ SFPendingMember(self.api, self.id).from_json(f) for f in json['pending']
                                  ])
        self._caller_permissions = frozenset([ Permission(p) for p in json['caller_effective_permissions'] ])
        return self

    def load(self):
        data = self.api.get_shared_folder(self.id)
        self.from_json(data)

    def create(self, name):
        data = self.api.create_shared_folder(name)
        self.from_json(data)