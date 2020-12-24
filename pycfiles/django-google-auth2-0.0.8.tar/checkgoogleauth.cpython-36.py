# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/GoogleAuthenticatorPyPI/django_google_auth/google/checkgoogleauth/checkgoogleauth.py
# Compiled at: 2019-04-01 23:12:51
# Size of source mod 2**32: 674 bytes
from django_google_auth.models import DjangoGoogleAuthenticator2
import pyotp

def check_google_auth(user, code):
    """
    验证google令牌
    :param user: 邮箱
    :param code: 客服端动态码
    :return: True/False
    """
    queryset_user = DjangoGoogleAuthenticator2.objects.filter(username=user)
    if not queryset_user.exists():
        return '{}用户未绑定google令牌'.format(user)
    else:
        obj_user = queryset_user.first()
        key = obj_user.key
        t = pyotp.TOTP(key)
        result = t.verify(code)
        res = result if result is True else False
        return res