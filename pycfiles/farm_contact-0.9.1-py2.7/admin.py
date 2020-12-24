# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contact/admin.py
# Compiled at: 2014-03-26 08:39:13
from django.contrib import admin
from .models import Enquiry, EnquiryType

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'ip', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


class EnquiryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(EnquiryType, EnquiryTypeAdmin)