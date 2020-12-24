# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/sf3/apps/django-auditware/auditware/admin.py
# Compiled at: 2016-04-05 16:17:06
# Size of source mod 2**32: 840 bytes
from django.db import models
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import UserAudit

class UserAuditAdmin(admin.ModelAdmin):
    formfield_overrides = {models.CharField: {'widget': forms.TextInput(attrs={'size': 160})}}
    list_display = [
     'id',
     'user',
     'audit_key',
     'ip_address',
     'user_agent',
     'referrer',
     'last_page',
     'pages_viwed',
     'force_logout',
     'updated_at',
     'created_at']
    search_fields = [
     'user__username',
     'ip_address',
     'user_agent',
     'referrer']
    list_per_page = 25


admin.site.register(UserAudit, UserAuditAdmin)