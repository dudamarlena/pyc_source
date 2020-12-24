# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Dropbox/Sites/dev_reactor/django-reactor/manifest/messages.py
# Compiled at: 2019-10-15 15:31:29
# Size of source mod 2**32: 1166 bytes
""" Manifest Messages
"""
import django.utils.translation as _
AUTH_LOGIN_SUCCESS = _('User logged in.')
AUTH_LOGOUT_SUCCESS = _('User logged out.')
AUTH_REGISTER_SUCCESS = _('User registered.')
AUTH_REGISTER_ERROR = _('Registration failed.')
AUTH_REGISTER_FORBIDDEN = _('Registration forbidden.')
AUTH_ACTIVATE_SUCCESS = _('Account activated.')
AUTH_ACTIVATE_ERROR = _('Activation failed!')
PASSWORD_RESET_SUCCESS = _('Password reset sent.')
PASSWORD_RESET_VERIFY_SUCCESS = _('Token verified.')
PASSWORD_RESET_VERIFY_ERROR = _('Verification failed.')
PASSWORD_RESET_CONFIRM_SUCCESS = _('New password saved.')
PASSWORD_RESET_CONFIRM_ERROR = _('Password reset failed.')
PASSWORD_CHANGE_SUCCESS = _('Password changed.')
EMAIL_CHANGE_SUCCESS = _('Email changed.')
EMAIL_CHANGE_CONFIRM_SUCCESS = _('Email confirmed.')
EMAIL_CHANGE_CONFIRM_ERROR = _('Confirmation failed.')
PROFILE_UPDATE_SUCCESS = _('Profile updated.')
REGION_UPDATE_SUCCESS = _('Regional settings updated.')
PICTURE_UPLOAD_SUCCESS = _('Picture uploaded.')
EMAIL_IN_USE_MESSAGE = _('This email address is already in use. Please supply a different email.')