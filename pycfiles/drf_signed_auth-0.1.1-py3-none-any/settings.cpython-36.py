# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcgibbons/projects/drf_signed_auth/drf_signed_auth/settings.py
# Compiled at: 2017-09-30 09:22:49
# Size of source mod 2**32: 596 bytes
"""
Contains app-settings imported from Django with default values
"""
from django.conf import settings
from rest_framework import permissions
SIGNED_URL_TTL = getattr(settings, 'SIGNED_URL_TTL', 30)
SIGNED_URL_QUERY_PARAM = getattr(settings, 'SIGNED_URL_QUERY_PARAM', 'sig')
SIGNED_URL_PERMISSION_CLASSES = getattr(settings, 'SIGNED_URL_PERMISSION_CLASSES', [
 permissions.IsAuthenticated])