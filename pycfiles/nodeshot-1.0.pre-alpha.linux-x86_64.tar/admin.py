# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/services/admin.py
# Compiled at: 2014-05-08 09:11:12
from django.contrib import admin
from django.conf import settings
from nodeshot.core.base.admin import BaseAdmin, BaseStackedInline
from .models import Category, Service, ServiceLogin, Url

class CategoryAdmin(BaseAdmin):
    list_display = ('name', 'description', 'added', 'updated')
    ordering = ('name', )
    search_fields = ('name', 'description')


class UrlInline(BaseStackedInline):
    model = Url
    if 'grappelli' in settings.INSTALLED_APPS:
        raw_id_fields = ('ip', )
        autocomplete_lookup_fields = {'fk': [
                'ip']}


class ServiceLoginInline(BaseStackedInline):
    model = ServiceLogin


class ServiceAdmin(BaseAdmin):
    list_display = ('name', 'device', 'category', 'access_level', 'status', 'is_published',
                    'added', 'updated')
    list_filter = ('category', 'status', 'is_published')
    search_fields = ('name', 'description', 'documentation_url')
    inlines = (UrlInline, ServiceLoginInline)
    raw_id_fields = ('device', )
    autocomplete_lookup_fields = {'fk': ('device', )}
    html_editor_fields = [
     'description']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)