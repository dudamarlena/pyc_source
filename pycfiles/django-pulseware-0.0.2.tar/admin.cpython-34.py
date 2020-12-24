# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.mpro-virenv/sf3/lib/python3.4/site-packages/pulseware/admin.py
# Compiled at: 2016-01-18 12:22:54
# Size of source mod 2**32: 240 bytes
from django.contrib import admin
from .models import Heartbeat

class HeartbeatAdmin(admin.ModelAdmin):
    list_display = [
     'id',
     'updated_at']
    ordering = [
     'id']


admin.site.register(Heartbeat, HeartbeatAdmin)