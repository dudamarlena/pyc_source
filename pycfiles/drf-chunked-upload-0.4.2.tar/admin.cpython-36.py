# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/phoetrymaster/Development/CSAR/drf-chunked-upload/drf_chunked_upload/admin.py
# Compiled at: 2015-03-15 14:48:41
# Size of source mod 2**32: 431 bytes
from django.contrib import admin
from .models import ChunkedUpload
from .settings import ABSTRACT_MODEL
if not ABSTRACT_MODEL:

    class ChunkedUploadAdmin(admin.ModelAdmin):
        list_display = ('id', 'filename', 'user', 'status', 'created_at')
        search_fields = ('filename', )
        list_filter = ('status', )


    admin.site.register(ChunkedUpload, ChunkedUploadAdmin)