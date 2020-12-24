# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flaviocaetano/github/pelican_admin/pelican_admin/admin/settings_admin.py
# Compiled at: 2012-12-10 08:42:46
__author__ = 'Flavio'
from django.contrib import admin
from ..models import Settings

class SettingsAdmin(admin.ModelAdmin):
    fields = [
     'name', 'value']
    list_display = ['name', 'value']
    ordering = ['name']
    search_fields = ['name', 'value']
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return ['name']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Settings, SettingsAdmin)