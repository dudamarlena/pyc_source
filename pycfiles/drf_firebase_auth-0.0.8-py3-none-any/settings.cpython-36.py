# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /code/server/drf_firebase_auth/settings.py
# Compiled at: 2019-02-10 01:14:27
# Size of source mod 2**32: 1101 bytes
"""
Settings config for the drf_firebase_auth application
Author: Gary Burgmann
Email: garyburgmann@gmail.com
Location: Springfield QLD, Australia
Last update: 2019-02-10
"""
import datetime
from django.conf import settings
from rest_framework.settings import APISettings
USER_SETTINGS = getattr(settings, 'DRF_FIREBASE_AUTH', None)
DEFAULTS = {'FIREBASE_SERVICE_ACCOUNT_KEY':'', 
 'FIREBASE_CREATE_LOCAL_USER':True, 
 'FIREBASE_ATTEMPT_CREATE_WITH_DISPLAY_NAME':True, 
 'FIREBASE_AUTH_HEADER_PREFIX':'JWT', 
 'FIREBASE_CHECK_JWT_REVOKED':True, 
 'FIREBASE_AUTH_EMAIL_VERIFICATION':False}
IMPORT_STRINGS = ()
api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)