# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/customcontent/admin.py
# Compiled at: 2011-05-29 08:44:55
from django.contrib import admin
from customcontent.models import CustomContent, CustomItem

class ItemAdmin(admin.ModelAdmin):
    pass


class ItemInline(admin.StackedInline):
    model = CustomItem
    fieldsets = (
     (
      None,
      {'fields': (('container_tag', 'container_id', 'container_classes'), 'code')}),
     (
      'Middleware positioning',
      {'fields': (('target_element', 'target_position'), ), 
         'classes': [
                   'collapse']}))


class ContentAdmin(admin.ModelAdmin):
    inlines = [
     ItemInline]
    fieldsets = (
     (
      None,
      {'fields': (
                  'name', ('is_active', 'preview'))}),
     (
      'Matching - URL or for Content object',
      {'fields': (
                  ('match_format', 'path_to_match'),
                  ('content_type', 'object_id'))}),
     (
      'Extra code for all items',
      {'fields': (
                  'extra_head', ('css', 'js')), 
         'classes': [
                   'collapse']}))


admin.site.register(CustomContent, ContentAdmin)
admin.site.register(CustomItem, ItemAdmin)