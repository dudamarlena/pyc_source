# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/imposeren/kava/42-kavyarnya/.env/lib/python2.7/site-packages/x_file_accel_redirects/admin.py
# Compiled at: 2014-03-28 02:58:14
from django.contrib import admin
from .models import AccelRedirect

class AccelRedirectAdmin(admin.ModelAdmin):
    list_display = ('description', 'login_required', 'prefix', 'internal_path', 'serve_document_root')
    list_filter = ('login_required', 'filename_solver')
    search_fields = ('description', 'prefix', 'internal_path', 'serve_document_root')


admin.site.register(AccelRedirect, AccelRedirectAdmin)