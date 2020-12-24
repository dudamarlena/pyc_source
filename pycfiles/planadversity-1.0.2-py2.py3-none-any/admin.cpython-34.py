# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/planadversity/planadversity/apps/meditations/admin.py
# Compiled at: 2014-12-29 17:58:19
# Size of source mod 2**32: 139 bytes
from django.contrib import admin
from .models import Meditation, Response
admin.site.register(Meditation)
admin.site.register(Response)