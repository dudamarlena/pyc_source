# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/app_plugins/admin.py
# Compiled at: 2008-10-17 00:15:13
from django.contrib import admin
from app_plugins.models import PluginPoint, Plugin, UserPluginPreference
from app_plugins.forms import AdminPluginPointForm, AdminPluginForm

class PluginPointAdmin(admin.ModelAdmin):
    list_display = ('label', 'index', 'registered', 'status')
    list_filter = ('registered', 'status')
    form = AdminPluginPointForm


class PluginAdmin(admin.ModelAdmin):
    list_display = ('label', 'index', 'registered', 'required', 'status')
    list_filter = ('registered', 'status')
    form = AdminPluginForm


class UserPluginPreferenceAdmin(admin.ModelAdmin):
    list_display = ('plugin', 'user', 'index', 'visible')
    list_filter = ('visible', )


admin.site.register(PluginPoint, PluginPointAdmin)
admin.site.register(Plugin, PluginAdmin)
admin.site.register(UserPluginPreference, UserPluginPreferenceAdmin)