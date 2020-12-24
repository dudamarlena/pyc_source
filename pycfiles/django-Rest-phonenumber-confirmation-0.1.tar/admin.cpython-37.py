# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/admin.py
# Compiled at: 2020-04-03 10:56:24
# Size of source mod 2**32: 567 bytes
from django.contrib import admin
from .models import PhoneNumber, PhoneNumberConfirmation

class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone', 'user', 'primary', 'verified')
    list_filter = ('primary', 'verified')
    raw_id_fields = ('user', )


class PhoneNumberConfirmationAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'sent', 'pin')
    list_filter = ('sent', )
    raw_id_fields = ('phone_number', )


admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(PhoneNumberConfirmation, PhoneNumberConfirmationAdmin)