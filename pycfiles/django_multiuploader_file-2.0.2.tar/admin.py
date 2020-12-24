# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matheus/Documents/projects/enki/Admin-Django/msk/multiuploader/admin.py
# Compiled at: 2013-04-04 15:38:21
from models import File
from django.contrib import admin

class FileAdmin(admin.ModelAdmin):
    search_fields = [
     'filename', 'key_data']
    list_display = ['filename', 'image', 'key_data']
    list_filter = ['filename', 'image', 'key_data']


admin.site.register(File, FileAdmin)