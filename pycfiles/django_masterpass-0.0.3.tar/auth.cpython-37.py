# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/user/src/django-masterpass/proj/django_masterpass/auth.py
# Compiled at: 2018-10-18 07:43:38
# Size of source mod 2**32: 1271 bytes
import warnings
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
UserModel = get_user_model()

class MasterPass(ModelBackend):

    def __init__(self):
        try:
            self.master_pass = getattr(settings, 'MASTER_PASS')
        except AttributeError:
            warnings.warn('you use django_masterpass, but not set MASTER_PASS value in settings')
            self.master_pass = None

        super(MasterPass, self).__init__()

    def __getattribute__(self, name):
        if name == 'authenticate':
            if not self.master_pass:
                return
        return super(MasterPass, self).__getattribute__(name)

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not self.master_pass:
            return
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            return
        else:
            if check_password(password, make_password(self.master_pass)):
                return user
            return