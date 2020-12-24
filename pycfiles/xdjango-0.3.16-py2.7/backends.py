# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdjango/contrib/auth/backends.py
# Compiled at: 2016-06-20 12:45:24
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class AntiBruteForceModelBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL preventing brute-force attacks.
    UserModel must have 'failed_login_attempts' field
    """
    MAX_FAIL_LOGIN_ATTEMPTS = 50

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if not user.failed_login_attempts < self.MAX_FAIL_LOGIN_ATTEMPTS:
                user.set_password(None)
                user.initialize_failed_attempts_counter()
                return
            if user.check_password(password):
                user.initialize_failed_attempts_counter()
                return user
            user.increment_failed_attempts_counter()
        except UserModel.DoesNotExist:
            pass

        UserModel().set_password(password)
        return