# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/backends.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 2003 bytes
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.contrib.auth.models import Permission
from aparnik.settings import aparnik_settings
from aparnik.contrib.users.models import DeviceLogin
from aparnik.utils.utils import convert_iran_phone_number_to_world_number
import logging
User = get_user_model()

class AuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            username = convert_iran_phone_number_to_world_number(username)
            user = User._default_manager.get_by_natural_key(username)
        except User.DoesNotExist:
            User().set_password(password)
        else:
            is_correct_password = False
            if aparnik_settings.USER_LOGIN_WITH_PASSWORD:
                is_correct_password = user.passwd == password
            else:
                is_correct_password = user.OTAVerify(password)
            if user.is_can_login():
                if is_correct_password:
                    user.last_login = now()
                    user.save()
                    return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(sys_id=user_id)
            if user.is_active:
                return user
            return
        except User.DoesNotExist:
            logging.getLogger('error_logger').error('user with %(user_id)d not found')
            return