# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/group.py
# Compiled at: 2016-01-12 12:25:49
from .interface import APIObject
from .interface import readonly

@readonly('id', sync=False)
@readonly('name')
@readonly('members')
class Group(APIObject):

    def __init__(self, api, gid=None):
        super(Group, self).__init__(api)
        self._id = gid
        self._name = None
        self._members = None
        return

    def from_json(self, json):
        self._id = json['id']
        self._name = json['name']
        from .group_member import GroupMember
        self._members = frozenset([ GroupMember(self.api, self.id).from_json(f) for f in json['members']
                                  ])
        return self

    def load(self):
        data = self.api.get_group(self.id)
        self.from_json(data)

    def create(self, name):
        data = self.api.create_group(name)
        self.from_json(data)

    def delete(self):
        self.api.delete_group(self.id)