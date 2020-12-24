# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jmcarp/miniconda/envs/guardian/lib/python2.7/site-packages/guardrail/ext/django/backends.py
# Compiled at: 2015-04-02 00:57:09
"""Custom object permissions backend for Django plugin"""
from .models import DjangoPermissionManager

class ObjectPermissionBackend(object):
    """Custom authentication backend for object-level permissions. Must be used
    in conjunction with a backend that handles the `authenticate` and `get_user`
    methods, such as the default `django.contrib.auth.backends.ModelBackend`.
    """

    def authenticate(self, username=None, password=None, *kwargs):
        return

    def get_user(self, user_id):
        return

    def has_perm(self, user, perm, target=None):
        manager = DjangoPermissionManager()
        return manager.has_permission(user, target, perm)

    def get_all_permissions(self, user, target=None):
        manager = DjangoPermissionManager()
        return manager.get_permissions(user, target)