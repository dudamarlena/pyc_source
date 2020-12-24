# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikehearing/GIT/django-hats/django_hats/context_processors.py
# Compiled at: 2017-07-02 03:21:35
# Size of source mod 2**32: 946 bytes
from django_hats.roles import RoleFinder

class RolesLookup(object):

    def __init__(self, user):
        self.user = user
        self._cache = {}

    def __getitem__(self, role_name):
        if self._cache.get(role_name, None) is None:
            role = RoleFinder.by_name(role_name)
            self._cache[role.get_slug()] = role.check_membership(self.user) if role is not None else False
        return self._cache[role_name]

    def __contains__(self, role):
        return self[role]


def roles(request):
    if hasattr(request, 'user'):
        user = request.user
    else:
        from django.contrib.auth.models import AnonymousUser
        user = AnonymousUser()
    return {'roles': RolesLookup(user)}