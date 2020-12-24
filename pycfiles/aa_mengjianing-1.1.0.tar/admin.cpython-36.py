# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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