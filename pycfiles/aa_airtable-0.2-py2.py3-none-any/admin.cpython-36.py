# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./../aa_airtable/admin.py
# Compiled at: 2017-06-21 21:50:37
# Size of source mod 2**32: 401 bytes
from django.contrib import admin
from aa_airtable.models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('created', 'status')
    list_filter = ['status']
    read_only_fields = ['status', 'error', 'file', 'user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(Job, JobAdmin)