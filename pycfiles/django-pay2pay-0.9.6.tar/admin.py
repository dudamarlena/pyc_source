# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-smsaero/smsaero/admin.py
# Compiled at: 2013-05-29 12:06:29
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