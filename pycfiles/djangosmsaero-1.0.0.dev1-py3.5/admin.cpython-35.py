# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smsaero/admin.py
# Compiled at: 2016-11-05 19:30:08
# Size of source mod 2**32: 595 bytes
from django.contrib import admin
from .models import Signature
from .models import SMSMessage

class SMSMessageAdmin(admin.ModelAdmin):
    list_display = ('phone', 'status', 'signature', 'sms_id', 'created')
    list_filter = ('signature', 'status', 'created')
    list_display_links = ('signature', )
    search_fields = ('text', 'signature__name')
    can_delete = False

    def has_add_permission(self, request):
        return False


admin.site.register(Signature)
admin.site.register(SMSMessage, SMSMessageAdmin)