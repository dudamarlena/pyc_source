# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_accounts_light/api/v1/errors.py
# Compiled at: 2018-11-12 18:25:32
# Size of source mod 2**32: 2533 bytes
from django.utils.translation import ugettext as _
BASE_ERROR_CODE = 499264
USER_ALREADY_LOGGED_IN = {'code': BASE_ERROR_CODE | 1, 
 'message': _('The user is already logged in')}
USER_ALREADY_EXIST = {'code': BASE_ERROR_CODE | 2, 
 'message': _('The user already exist')}
THE_PASSWORD_IS_NOT_SECURE = {'code': BASE_ERROR_CODE | 3, 
 'message': _('The password is not secure')}
INVALID_EMAIL = {'code': BASE_ERROR_CODE | 4, 
 'message': _('The email is not valid')}
SIGNUPS_DISABLED = {'code': BASE_ERROR_CODE | 5, 
 'message': _('Signups are currently disabled')}
EMAIL_LOGIN_DISABLED = {'code': BASE_ERROR_CODE | 6, 
 'message': _('Email login is disabled')}
WRONG_CREDENTIALS = {'code': BASE_ERROR_CODE | 7, 
 'message': _('Wrong credentials')}
PASSWORD_RESET_IDENTITY_AND_CODE_CANT_BE_BOTH_EMPTY = {'code': BASE_ERROR_CODE | 8, 
 'message': _("Identity and code can't be both empty")}
PASSWORD_RESET_INVALID = {'code': BASE_ERROR_CODE | 9, 
 'message': _('Password reset invalid')}
PASSWORD_RESET_ALREADY_ACTIVATED = {'code': BASE_ERROR_CODE | 10, 
 'message': _('Password reset already activated')}
SIGNUP_PIPELINE_FAILED = {'code': BASE_ERROR_CODE | 11, 
 'message': _('Signup pipeline failed')}
SIGNUP_FAILED = {'code': BASE_ERROR_CODE | 12, 
 'message': _('Signup failed')}
INVALID_FACEBOOK_ACCESS_TOKEN = {'code': BASE_ERROR_CODE | 13, 
 'message': _('Invalid facebook access token')}
FACEBOOK_CONNECTION_ERROR = {'code': BASE_ERROR_CODE | 14, 
 'message': _('Facebook connection error')}
FACEBOOK_EMAIL_PERMISSION_NOT_SETTED = {'code': BASE_ERROR_CODE | 15, 
 'message': _('Facebook email permission not setted')}
INVALID_GOOGLE_PLUS_ACCESS_TOKEN = {'code': BASE_ERROR_CODE | 16, 
 'message': _('Invalid google plus access token')}
GOOGLE_PLUS_CONNECTION_ERROR = {'code': BASE_ERROR_CODE | 17, 
 'message': _('Google Plus connection error')}
GOOGLE_PLUS_NO_EMAILS_ASSOCIATED_WITH_THE_ACCOUNT = {'code': BASE_ERROR_CODE | 18, 
 'message': _('Google Plus no emails associated with the account')}
SIGNUP_FAILED_DUE_TO_TOKEN = {'code': BASE_ERROR_CODE | 19, 
 'message': _('Signup failed due to token')}
LOGIN_FAILED = {'code': BASE_ERROR_CODE | 20, 
 'message': _('Login failed')}
LOGIN_FAILED_DUE_TO_TOKEN = {'code': BASE_ERROR_CODE | 21, 
 'message': _('Login failed due to token')}
FACEBOOK_ERROR_VALIDATING_ACCESS_TOKEN = {'code': BASE_ERROR_CODE | 22, 
 'message': _('The user has not authorized application')}