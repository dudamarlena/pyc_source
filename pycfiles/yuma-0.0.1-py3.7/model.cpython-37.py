# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\yuma\model.py
# Compiled at: 2020-01-15 20:31:33
# Size of source mod 2**32: 1721 bytes


class Permission:
    __doc__ = '\n    Permission entity\n    '
    id = 0
    key = ''
    memo = ''
    father_id = -1

    def __init__(self, permission_id: int, key: str, memo: str, father_id: int=-1):
        """
        Initialize with value
        :param permission_id: Permission id
        :param key: Permission key
        :param memo: Permission memo
        :param father_id: Father permission id
        """
        self.id = permission_id
        self.key = key
        self.memo = memo
        self.father_id = father_id


class PermissionGroup:
    __doc__ = '\n    Collection of multiple permissions\n    '
    key = ''
    _ids = []

    def __init__(self, key):
        """
        Initializing PermissionGroup
        :param key: Group key
        """
        self.key = key

    def add_id(self, permission_id: int):
        """
        Add id to permission group
        :param permission_id: permission id
        :return: self
        """
        self._ids.append(permission_id)
        return self

    def add_ids(self, permission_ids):
        """
        Add id list to permission group
        :param permission_ids: permission_ids
        :return: self
        """
        self._ids = self._ids + permission_ids
        return self

    def have(self, permission_id):
        """
        Check if there is an ID entered in the group
        :param permission_id: permission_id
        :return: Bool
        """
        return permission_id in self._ids