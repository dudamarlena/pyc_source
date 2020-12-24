# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/core/auth_backends.py
# Compiled at: 2016-05-20 23:41:38
from __future__ import unicode_literals
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.utils.http import base36_to_int
from wenlincms.utils.models import get_user_model
User = get_user_model()

class wenlincmsBackend(ModelBackend):
    """
    Extends Django's ``ModelBackend`` to allow login via username,
    email, or verification token.

    Args are either ``username`` and ``password``, or ``uidb36``
    and ``token``. In either case, ``is_active`` can also be given.

    For login, is_active is not given, so that the login form can
    raise a specific error for inactive users.
    For password reset, True is given for is_active.
    For signup verficiation, False is given for is_active.
    """

    def authenticate(self, **kwargs):
        if kwargs:
            username = kwargs.pop(b'username', None)
            if username:
                username_or_email = Q(username=username) | Q(email=username)
                password = kwargs.pop(b'password', None)
                try:
                    user = User.objects.get(username_or_email, **kwargs)
                except User.DoesNotExist:
                    pass
                else:
                    if user.check_password(password):
                        return user

            else:
                if b'uidb36' not in kwargs:
                    return
                kwargs[b'id'] = base36_to_int(kwargs.pop(b'uidb36'))
                token = kwargs.pop(b'token')
                try:
                    user = User.objects.get(**kwargs)
                except User.DoesNotExist:
                    pass
                else:
                    if default_token_generator.check_token(user, token):
                        return user

        return