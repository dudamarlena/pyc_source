# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/twiliobox/admin.py
# Compiled at: 2014-08-27 19:26:12
from django.contrib import admin
from twiliobox.models import TwilioNumber

class TwilioNumberAdmin(admin.ModelAdmin):
    list_editable = [
     'is_default_account']
    list_display = ['phone_number', 'is_default_account']
    save_on_top = True


admin.site.register(TwilioNumber, TwilioNumberAdmin)