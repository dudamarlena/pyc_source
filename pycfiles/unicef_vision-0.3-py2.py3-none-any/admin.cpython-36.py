# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/vision/src/unicef_vision/admin.py
# Compiled at: 2019-02-05 11:28:31
# Size of source mod 2**32: 595 bytes
from django.contrib import admin

class VisionLoggerAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    list_filter = ('handler_name', 'successful', 'date_processed')
    list_display = ('handler_name', 'total_records', 'total_processed', 'successful',
                    'date_processed')
    readonly_fields = ('details', 'handler_name', 'total_records', 'total_processed',
                       'successful', 'exception_message', 'date_processed')