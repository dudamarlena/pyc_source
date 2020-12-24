# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/admin.py
# Compiled at: 2017-04-18 19:01:48
# Size of source mod 2**32: 496 bytes
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from google_address.models import Address

class GoogleAddressAdmin(admin.ModelAdmin):
    fields = [
     'id', 'raw', 'raw2']
    list_display = [
     'id', 'raw', 'raw2']
    list_filter = []
    list_editable = []
    search_fields = [
     'raw', 'raw2', 'address_line']
    readonly_fields = [
     'id']
    raw_id_fields = []


admin.site.register(Address, GoogleAddressAdmin)