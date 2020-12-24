# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/admin.py
# Compiled at: 2016-09-25 10:50:25
from django.contrib import admin
from nodeconductor_organization.models import Organization, OrganizationUser

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'native_name', 'customer', 'uuid')
    list_filter = ('abbreviation', 'native_name')
    ordering = ('abbreviation', 'native_name', 'customer')


class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'organization')
    list_filter = ('is_approved', 'user')
    ordering = ('user', 'is_approved', 'organization')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)