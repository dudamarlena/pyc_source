# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_auth/djinn_auth/admin.py
# Compiled at: 2015-02-10 14:58:11
from django.contrib import admin
from djinn_auth.models.role import Role
from djinn_auth.models.localrole import LocalRole
from djinn_auth.models.globalrole import GlobalRole
from djinn_auth.models.localpermission import LocalPermission

class RoleAdmin(admin.ModelAdmin):
    list_display = [
     'name']
    search_fields = ['name']
    ordering = ['-name']


class LocalRoleAdmin(admin.ModelAdmin):
    list_display = [
     'role', 'instance_ct', 'instance_id', 'assignee_id',
     'assignee_ct']
    list_filter = ['role', 'instance_ct', 'assignee_ct']
    search_fields = ['role__name']


class GlobalRoleAdmin(admin.ModelAdmin):
    pass


class LocalPermissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Role, RoleAdmin)
admin.site.register(LocalRole, LocalRoleAdmin)
admin.site.register(GlobalRole, GlobalRoleAdmin)
admin.site.register(LocalPermission, LocalPermissionAdmin)