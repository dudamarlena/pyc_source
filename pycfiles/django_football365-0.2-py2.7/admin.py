# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/football365/admin.py
# Compiled at: 2013-05-21 11:00:49
from django.contrib import admin
from football365.models import Call

class CallAdmin(admin.ModelAdmin):
    list_display = ('title', 'call_type', 'football365_service_id')


admin.site.register(Call, CallAdmin)