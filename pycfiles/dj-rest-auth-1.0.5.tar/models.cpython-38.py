# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michael/Projects/dj-rest-auth/dj_rest_auth/models.py
# Compiled at: 2020-04-16 02:58:10
# Size of source mod 2**32: 200 bytes
from django.conf import settings
from django.utils.module_loading import import_string
TokenModel = import_string(getattr(settings, 'REST_AUTH_TOKEN_MODEL', 'rest_framework.authtoken.models.Token'))