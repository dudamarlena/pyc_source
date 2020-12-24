# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\django_twilio_sms\admin.py
# Compiled at: 2013-06-20 03:15:21
from __future__ import unicode_literals
from django.contrib import admin
from .models import IncomingSMS, OutgoingSMS

class IncomingSMSAdmin(admin.ModelAdmin):
    list_display = [
     b'sms_sid', b'account_sid',
     b'from_number', b'from_city', b'from_state', b'from_zip', b'from_country',
     b'to_number', b'body',
     b'created_at']
    list_filter = [
     b'to_number', b'from_country', b'from_state', b'from_city']
    search_fields = [b'from_number', b'body']


class OutgoingSMSAdmin(admin.ModelAdmin):
    list_display = [
     b'id', b'sms_sid', b'account_sid',
     b'from_number', b'to_number', b'to_parsed',
     b'body',
     b'created_at', b'sent_at', b'delivered_at', b'status',
     b'price', b'price_unit']
    list_filter = [
     b'from_number', b'status']
    search_fields = [b'to_number', b'body']


admin.site.register(IncomingSMS, IncomingSMSAdmin)
admin.site.register(OutgoingSMS, OutgoingSMSAdmin)