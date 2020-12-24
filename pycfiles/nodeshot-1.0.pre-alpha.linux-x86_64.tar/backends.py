# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/profiles/backends.py
# Compiled at: 2015-03-02 10:21:03
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Authenticates against user email.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        usermodel = get_user_model()
        try:
            user = usermodel.objects.get(email=username)
            if user.check_password(password):
                return user
        except usermodel.DoesNotExist:
            return

        return