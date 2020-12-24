# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cytomine/models/user.py
# Compiled at: 2017-09-05 05:52:58
__author__ = 'Stévens Benjamin <b.stevens@ulg.ac.be>'
__contributors__ = ['Marée Raphaël <raphael.maree@ulg.ac.be>', 'Rollus Loïc <lrollus@ulg.ac.be']
__copyright__ = 'Copyright 2010-2015 University of Liège, Belgium, http://www.cytomine.be/'
from model import Model
from collection import Collection

class User(Model):

    def __init__(self, params=None):
        super(User, self).__init__(params)
        self._callback_identifier = 'user'

    def to_url(self):
        if hasattr(self, 'id'):
            return 'user/%d.json' % self.id
        else:
            if hasattr(self, 'software'):
                self._callback_identifier = 'userJob'
                return 'userJob.json'
            if hasattr(self, 'current'):
                return 'user/current.json'
            return 'user.json'

    def __str__(self):
        return 'User : ' + str(self.id)


class Group(Model):

    def __init__(self, params=None):
        super(Group, self).__init__(params)
        self._callback_identifier = 'group'

    def to_url(self):
        if hasattr(self, 'id'):
            return 'group/%d.json' % self.id
        else:
            return 'group.json'

    def __str__(self):
        return 'group : ' + str(self.id)


class UserGroup(Model):

    def __init__(self, params=None):
        super(UserGroup, self).__init__(params)
        self._callback_identifier = 'usergroup'

    def to_url(self):
        if hasattr(self, 'user') and not hasattr(self, 'id'):
            return 'user/%d/group.json' % self.user
        if hasattr(self, 'user') and hasattr(self, 'group'):
            return 'user/%d/group/%d.json' % (self.user, self.group)
        if not hasattr(self, 'user') and hasattr(self, 'group'):
            return 'group/%d.json' % self.group

    def __str__(self):
        return 'UserGroup : ' + str(self.id)


class Role(Model):

    def __init__(self, params=None):
        super(Role, self).__init__(params)

    def to_url(self):
        if hasattr(self, 'id'):
            return 'role/%d.json' % self.id
        else:
            return 'role.json'

    def __str__(self):
        return 'Role : ' + str(self.id)


class UserRole(Model):

    def __init__(self, params=None):
        super(UserRole, self).__init__(params)
        self._callback_identifier = 'secusersecrole'

    def to_url(self):
        if hasattr(self, 'user') and not hasattr(self, 'id'):
            return 'user/%d/role.json' % self.user
        if hasattr(self, 'user') and hasattr(self, 'role'):
            return 'user/%d/role/%d.json' % (self.user, self.role)

    def __str__(self):
        return 'UserRole : ' + str(self.id)


class GroupCollection(Collection):

    def __init__(self, params=None):
        super(GroupCollection, self).__init__(Group, params)

    def to_url(self):
        if hasattr(self, 'group'):
            return 'group/' + str(self.group) + '.json'
        else:
            return 'group.json'


class UserRoleCollection(Collection):

    def __init__(self, params=None):
        super(UserRoleCollection, self).__init__(UserRole, params)

    def to_url(self):
        return 'user/%d/role.json' % self.user


class RoleCollection(Collection):

    def __init__(self, params=None):
        super(RoleCollection, self).__init__(Role, params)

    def to_url(self):
        return 'role.json'


class UserCollection(Collection):

    def __init__(self, params=None):
        super(UserCollection, self).__init__(User, params)

    def to_url(self):
        return 'user.json'