# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/devel/cfm/beehve/beehve/apps/workers/admin.py
# Compiled at: 2016-08-07 13:07:33
# Size of source mod 2**32: 131 bytes
from django.contrib import admin
from .models import Position, Worker
admin.site.register(Position)
admin.site.register(Worker)