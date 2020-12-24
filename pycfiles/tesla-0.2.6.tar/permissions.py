# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/AuthXpProjectName/authxpprojectname/model/permissions.py
# Compiled at: 2007-09-06 07:54:22
from elixir.ext.associable import associable
from elixir import events
from elixir.statements import Statement, STATEMENTS
from user import Permission
import types
_has_permissions = associable(Permission, '_permissions')

class HasPermissions(object):

    def __init__(self, entity, permissions, precheck=None, postcheck=None, default_permissions=None):
        entity._permission_names = permissions
        entity._permissions_precheck = precheck
        entity._permissions_postcheck = postcheck
        statements = getattr(entity, STATEMENTS, [])
        statements.append((_has_permissions, (), {}))
        setattr(entity, STATEMENTS, statements)

        @events.before_insert
        def create_permissions(self):
            for perm in entity._permission_names:
                if type(perm) is types.StringType:
                    name, description = perm, None
                elif type(perm) is types.TupleType:
                    (name, description) = perm
                self._permissions.append(Permission(name=name, description=description))

            if self.default_permissions:
                self.default_permissions()
            return

        def get_permission(self, name):
            for p in self._permissions:
                if name == p.name:
                    return p

        def get_permissions(self, *names):
            if names:
                return [ p for p in self._permissions if p.name in names ]
            return self._permissions

        def grant_permissions_for_user(self, user, *names):
            for p in self.get_permissions(*names):
                user.user_permissions.append(p)

        def grant_permissions_for_group(self, group, *names):
            for p in self.get_permissions(*names):
                group.permissions.append(p)

        def revoke_permissions_for_user(self, user, *names):
            for p in self.get_permissions(*names):
                if p in user.user_permissions:
                    user.user_permissions.remove(p)

        def revoke_permissions_for_group(self, group, *names):
            for p in self.get_permissions(*names):
                if p in group.permissions:
                    group.permissions.remove(p)

        def has_permission(self, principal, perm):
            if entity._permissions_precheck:
                precheck = getattr(self, entity._permissions_precheck)
                if precheck and precheck(principal, perm):
                    return True
            permission = self.get_permission(perm)
            if permission and permission in principal.permissions:
                return True
            if entity._permissions_postcheck:
                postcheck = getattr(self, entity._permissions_postcheck)
                if postcheck and postcheck(principal, perm):
                    return True
            return False

        entity.create_permissions = create_permissions
        entity.default_permissions = default_permissions
        entity.get_permission = get_permission
        entity.get_permissions = get_permissions
        entity.grant_permissions_for_user = grant_permissions_for_user
        entity.grant_permissions_for_group = grant_permissions_for_group
        entity.revoke_permissions_for_user = revoke_permissions_for_user
        entity.revoke_permissions_for_group = revoke_permissions_for_group
        entity.has_permission = has_permission


has_permissions = Statement(HasPermissions)
__all__ = [
 'has_permissions']