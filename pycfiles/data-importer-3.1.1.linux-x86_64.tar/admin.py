# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/admin.py
# Compiled at: 2020-04-17 10:46:24
from django.contrib import admin
from data_importer.models import FileHistory

class FileAdmin(admin.ModelAdmin):
    list_display = [
     'compose_file_name', 'updated_at', 'owner',
     'active', 'is_task', 'status', 'file_link']
    list_filter = ['is_task', 'active', 'status']
    search_fields = ['file_upload']


admin.site.register(FileHistory, FileAdmin)