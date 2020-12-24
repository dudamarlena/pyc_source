# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\backends\magic_link.py
# Compiled at: 2020-02-28 20:30:00
# Size of source mod 2**32: 849 bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from CustomAuth.tokens import magic_token

class MagicLinkBackend(BaseBackend):

    def get_user(self, uid64):
        try:
            uid = force_text(urlsafe_base64_decode(uid64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        return user

    def authenticate(self, request, uid64, token):
        user = self.get_user(uid64)
        if user is not None:
            if magic_token.check_token(user, token):
                return user
        return