# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbotext/admin.py
# Compiled at: 2018-07-31 04:09:55
from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.contrib import admin
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from reviewboard.extensions.base import get_extension_manager
from reviewbotext.extension import ReviewBotExtension
from reviewbotext.forms import ToolForm
from reviewbotext.models import Tool

class ToolAdmin(admin.ModelAdmin):
    """Admin site definitions for the Tool model."""
    form = ToolForm
    list_display = [
     b'name',
     b'version',
     b'in_last_update']
    list_filter = [
     b'in_last_update']
    ordering = [
     b'enabled',
     b'in_last_update',
     b'name',
     b'version']
    readonly_fields = [
     b'name',
     b'version',
     b'description',
     b'in_last_update',
     b'timeout']
    fieldsets = (
     (
      b'Tool Information',
      {b'fields': ('name', 'version', 'description', 'in_last_update', 'timeout'), 
         b'classes': ('wide', )}),)

    def refresh_tools_view(self, request, template_name=b'refresh.html'):
        Tool.objects.all().update(in_last_update=False)
        ReviewBotExtension.instance.send_refresh_tools()
        return render_to_response(template_name, RequestContext(request, {}, current_app=self.admin_site.name))

    def get_urls(self):
        urls = super(ToolAdmin, self).get_urls()
        my_urls = patterns(b'', url(b'^refresh/$', self.admin_site.admin_view(self.refresh_tools_view)))
        return my_urls + urls

    def has_add_permission(self, request):
        return False


extension_manager = get_extension_manager()
extension = extension_manager.get_enabled_extension(ReviewBotExtension.id)
extension.admin_site.register(Tool, ToolAdmin)