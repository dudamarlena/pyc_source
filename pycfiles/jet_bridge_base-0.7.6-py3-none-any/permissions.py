# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/permissions.py
# Compiled at: 2019-10-22 15:45:18
from jet_bridge_base.db import Session
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
        token = view.request.headers.get('AUTHORIZATION')
        session_create = not getattr(view, 'session')
        permission = view.required_project_permission() if hasattr(view, 'required_project_permission') else None
        if not token:
            return False
        else:
            try:
                session = Session() if session_create else getattr(view, 'session')
                if token[:len(self.token_prefix)] == self.token_prefix:
                    token = token[len(self.token_prefix):]
                    result = project_auth(session, token, permission)
                    if result.get('warning'):
                        view.headers['X-Application-Warning'] = result['warning']
                    return result['result']
                if token[:len(self.project_token_prefix)] == self.project_token_prefix:
                    token = token[len(self.project_token_prefix):]
                    result = project_auth(session, token, permission)
                    if result.get('warning'):
                        view.headers['X-Application-Warning'] = result['warning']
                    return result['result']
                return False
            finally:
                if session_create:
                    session.close()

            return


class ModifyNotInDemo(BasePermission):

    def has_permission(self, view):
        if not settings.READ_ONLY:
            return True
        if view.request.method.lower() in ('post', 'put', 'patch', 'delete'):
            return False
        return True