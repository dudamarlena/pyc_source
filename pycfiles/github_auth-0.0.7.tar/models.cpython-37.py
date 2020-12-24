# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\Desktop\programlarim\djangoapps\github-auth\github_auth\models.py
# Compiled at: 2019-09-02 16:04:05
# Size of source mod 2**32: 1006 bytes
import ast
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import django.utils.translation as _
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

class GithubAuthUser(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=(models.CASCADE))
    code = models.CharField(max_length=500,
      help_text=(_('github user code / to get access_token')))
    access_token = models.CharField(max_length=500,
      help_text=(_('github user access_token to any api operations')))
    extra_data = models.TextField()

    def __str__(self):
        return str(self.user)

    @property
    def get_extra_data_as_dict(self):
        return ast.literal_eval(self.extra_data)

    @property
    def avatar_url(self):
        return self.get_extra_data_as_dict.get('avatar_url')

    @property
    def username(self):
        return self.user.username