# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/admin.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.contrib import admin
from reviewboard.webapi.models import WebAPIToken

class WebAPITokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'local_site', 'time_added', 'last_updated')
    raw_id_fields = ('user', )


admin.site.register(WebAPIToken, WebAPITokenAdmin)