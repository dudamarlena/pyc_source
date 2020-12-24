# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cidiomar/DEV/atados/gpa.main/api/django-ovp-admin/ovp_admin/modules/user.py
# Compiled at: 2017-01-09 10:17:09
# Size of source mod 2**32: 723 bytes
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from ovp_users.models import User

class UserAdmin(admin.ModelAdmin):
    fields = [
     ('id', 'name', 'email'), 'slug', 'phone',
     ('is_staff', 'is_superuser', 'is_active', 'is_email_verified')]
    list_display = [
     'id', 'email', 'name', 'last_login', 'is_active', 'is_staff', 'is_email_verified']
    list_filter = [
     'is_active', 'is_staff', 'last_login', 'joined_date']
    list_editable = [
     'is_active', 'is_staff', 'is_email_verified']
    search_fields = [
     'email', 'name']
    readonly_fields = [
     'id']
    raw_id_fields = []


admin.site.register(User, UserAdmin)