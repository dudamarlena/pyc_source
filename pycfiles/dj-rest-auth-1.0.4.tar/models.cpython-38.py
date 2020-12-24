# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/circleci/project/dj_rest_auth/models.py
# Compiled at: 2020-03-01 00:55:19
# Size of source mod 2**32: 210 bytes
from django.conf import settings
import rest_framework.authtoken.models as DefaultTokenModel
TokenModel = getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel)