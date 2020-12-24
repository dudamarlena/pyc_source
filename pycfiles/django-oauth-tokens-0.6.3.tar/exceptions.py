# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-oauth-tokens/oauth_tokens/exceptions.py
# Compiled at: 2016-01-18 07:29:50


class LoginPasswordError(Exception):
    pass


class AccountLocked(Exception):
    pass


class WrongRedirectUrl(Exception):
    pass


class WrongAuthorizationResponseUrl(Exception):
    pass


class RedirectUriError(Exception):
    pass