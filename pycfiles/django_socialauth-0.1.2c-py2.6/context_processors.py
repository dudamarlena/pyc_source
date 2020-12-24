# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialauth/context_processors.py
# Compiled at: 2010-06-28 10:33:16
from django.conf import settings

def facebook_api_key(request):
    FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', '')
    FACEBOOK_API_KEY = getattr(settings, 'FACEBOOK_API_KEY', '')
    FACEBOOK_EXTENDED_PERMISSIONS = getattr(settings, 'FACEBOOK_EXTENDED_PERMISSIONS', '')
    if FACEBOOK_APP_ID:
        return {'FACEBOOK_APP_ID': FACEBOOK_APP_ID, 'FACEBOOK_API_KEY': FACEBOOK_API_KEY, 
           'login_button_perms': (',').join(FACEBOOK_EXTENDED_PERMISSIONS)}
    else:
        return {}