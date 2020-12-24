# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramzi/drf-social-auth/drf_social/admin.py
# Compiled at: 2020-03-05 03:56:09
# Size of source mod 2**32: 110 bytes
from django.contrib import admin
from drf_social.models import AuthProvider
admin.site.register(AuthProvider)