# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/permissions.py
# Compiled at: 2020-03-09 14:10:50
# Size of source mod 2**32: 2192 bytes
import json
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
        token = view.request.headers.get('AUTHORIZATION')
        permission = view.required_project_permission() if hasattr(view, 'required_project_permission') else None
        if not token:
            return False
        else:
            bridge_settings_encoded = view.request.headers.get('X_BRIDGE_SETTINGS')
            if bridge_settings_encoded:
                from jet_bridge_base.utils.crypt import decrypt
                try:
                    secret_key = settings.TOKEN.replace('-', '').lower()
                    bridge_settings = json.loads(decrypt(bridge_settings_encoded, secret_key))
                except Exception:
                    bridge_settings = {}

                project_token = bridge_settings.get('token')
            else:
                project_token = settings.TOKEN
            if token[:len(self.token_prefix)] == self.token_prefix:
                token = token[len(self.token_prefix):]
                result = project_auth(token, project_token, permission)
                return result['result']
            if token[:len(self.project_token_prefix)] == self.project_token_prefix:
                token = token[len(self.project_token_prefix):]
                result = project_auth(token, project_token, permission)
                return result['result']
            return False


class ReadOnly(BasePermission):

    def has_permission(self, view):
        if not settings.READ_ONLY:
            return True
        if view.action in ('create', 'update', 'partial_update', 'destroy'):
            return False
        return True