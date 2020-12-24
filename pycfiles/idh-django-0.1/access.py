# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\django\core\basic\access.py
# Compiled at: 2018-02-12 22:30:54
# Size of source mod 2**32: 4148 bytes
from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from idh.django.core.beans import Struct
from idh.django.core.formatter.base import Formatter
cache = None
if hasattr(settings, 'CACHE') and 'ACCESS' in settings.CACHE:
    cache = settings.CACHE['ACCESS']
ACCESS_KEY_PREFIX = 'KEY::'
ACCESS_KEY_EXPIRY = 3600

class UserParser(Formatter):

    def parse(self, in_user):
        return super(UserParser, self).fx_dumps(in_user)


class User(object):

    def __init__(self, obj=None, **kwargs):
        in_user = None
        if obj is not None:
            in_user = obj
        else:
            if 'user' in kwargs:
                in_user = kwargs['user']
            if in_user is None:
                raise Exception('user is required')
            if isinstance(in_user, AuthUser):
                group_permissions = in_user.get_group_permissions()
                myuser = UserParser().parse(in_user)
                myuser['group_permissions'] = list(group_permissions)
                user_permissions = []
                for perm in myuser['user_permissions']:
                    user_permissions.append(perm['content_type']['app_label'] + '.' + perm['codename'])

                user_permissions = list(set(user_permissions))
                myuser['user_permissions'] = user_permissions
                for group in myuser['groups']:
                    permissions = []
                    for perm in group['permissions']:
                        permissions.append(perm['content_type']['app_label'] + '.' + perm['codename'])

                    permissions = list(set(permissions))
                    group['permissions'] = permissions

            else:
                myuser = in_user
        if isinstance(myuser, Struct):
            myuser = myuser.__dict__
        self.__dict__.update(myuser)
        for k, v in myuser.items():
            if isinstance(v, dict):
                self.__dict__[k] = User(v)

    def get_group_permissions(self):
        return self.group_permissions

    def get_all_permissions(self):
        all_permissions = self.group_permissions + self.user_permissions
        return list(set(all_permissions))


class Access(object):

    def __init__(self, obj=None, **kwargs):
        if obj is not None:
            data = obj
        else:
            data = kwargs
        if 'user' in data:
            self.user = data['user']
        else:
            self.user = None
        if 'key' in data:
            self.key = data['key']
        else:
            self.key = None
        if 'secret' in data:
            self.secret = data['secret']
        else:
            self.secret = None

    def __iter__(self):
        yield ('user', self.user)
        yield ('key', self.key)
        yield ('secret', self.secret)

    def get(key):
        access = cache.get(ACCESS_KEY_PREFIX, key)
        if access is None:
            return
        access = eval(access)
        if 'user' in access:
            access['user'] = User(access['user'])
        else:
            access['user'] = None
        return Access(access)

    def create(key, access):
        data = dict(access.__dict__)
        if 'user' in data:
            if hasattr(data['user'], '__dict__'):
                data['user'] = data['user'].__dict__
        else:
            data['user'] = None
        return cache.set(ACCESS_KEY_PREFIX, key, data, ACCESS_KEY_EXPIRY)

    def revoke(key):
        return cache.delete(ACCESS_KEY_PREFIX, key)

    def touch(key):
        return cache.expire(ACCESS_KEY_PREFIX, key, ACCESS_KEY_EXPIRY)