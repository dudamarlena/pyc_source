# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/permissions.py
# Compiled at: 2019-11-15 01:53:19
# Size of source mod 2**32: 1601 bytes
from jet_bridge_base import settings
from jet_bridge_base.utils.backend import project_auth

class BasePermission(object):

    def has_permission(self, view):
        return True

    def has_object_permission(self, view, obj):
        return True


class HasProjectPermissions(BasePermission):
    token_prefix = 'Token '
    project_token_prefix = 'ProjectToken '

    def has_permission(self, view):
        return True
        permission = None
        if not token:
            return False
        if token[:len(self.token_prefix)] == self.token_prefix:
            token = token[len(self.token_prefix):]
            result = project_auth(token, permission)
            if result.get('warning'):
                view.headers['X-Application-Warning'] = result['warning']
            return result['result']
        else:
            if token[:len(self.project_token_prefix)] == self.project_token_prefix:
                token = token[len(self.project_token_prefix):]
                result = project_auth(token, permission)
                if result.get('warning'):
                    view.headers['X-Application-Warning'] = result['warning']
                return result['result']
            return False


class ReadOnly(BasePermission):

    def has_permission(self, view):
        if not settings.READ_ONLY:
            return True
        else:
            if view.action in ('create', 'update', 'partial_update', 'destroy'):
                return False
            return True