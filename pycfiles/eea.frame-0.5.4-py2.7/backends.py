# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/frame/backends.py
# Compiled at: 2017-04-19 09:40:55
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import Group

class FrameUserBackend(RemoteUserBackend):

    def clean_username(self, userdata):
        self._userdata = userdata
        return userdata.get('user_id')

    def configure_user(self, user):
        for role in self._userdata.get('user_roles', []):
            group, new = Group.objects.get_or_create(name=role)
            group.user_set.add(user)

        return user