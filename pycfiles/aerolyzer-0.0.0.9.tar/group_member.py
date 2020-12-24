# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/group_member.py
# Compiled at: 2016-03-28 13:15:32
from .interface import APIObject
from .interface import readonly

@readonly('group', sync=False)
@readonly('email', sync=False)
@readonly('first_name')
@readonly('last_name')
class GroupMember(APIObject):

    def __init__(self, api, gid, email=None):
        super(GroupMember, self).__init__(api)
        from .group import Group
        self._group = Group(self.api, gid)
        self._email = email
        self._first_name = None
        self._last_name = None
        return

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.group.id == other.group.id and self.email == other.email
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.group.id != other.group.id and self.email != other.email
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def from_json(self, json):
        self._email = json['email']
        self._first_name = json['first_name']
        self._last_name = json['last_name']
        return self

    def load(self):
        data = self.api.get_group_member(self.group.id, self.email)
        self.from_json(data)

    def create(self, email):
        data = self.api.add_group_member(self.group.id, email)
        self.from_json(data)

    def delete(self):
        self.api.remove_group_member(self.group.id, self.email)