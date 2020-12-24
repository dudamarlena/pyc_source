# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-admin/ovp_admin/modules/core/address.py
# Compiled at: 2017-01-10 11:12:37
# Size of source mod 2**32: 562 bytes
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from ovp_core.models import GoogleAddress

class GoogleAddressAdmin(admin.ModelAdmin):
    fields = [
     'id', 'typed_address', 'typed_address2']
    list_display = [
     'id', 'typed_address', 'typed_address2']
    list_filter = []
    list_editable = []
    search_fields = [
     'typed_address', 'typed_address2', 'address_line']
    readonly_fields = [
     'id']
    raw_id_fields = []


admin.site.register(GoogleAddress, GoogleAddressAdmin)