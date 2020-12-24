# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/GoogleAuthenticatorPyPI/django_google_auth/google/deletegoogleauth/deletegoogleauth.py
# Compiled at: 2019-04-01 23:13:09
# Size of source mod 2**32: 371 bytes
from django_google_auth.models import DjangoGoogleAuthenticator2

def delete_google_auth(user):
    """
    删除google令牌
    :param user: 邮箱
    :return: None
    """
    DjangoGoogleAuthenticator2.objects.filter(username=user).delete()