# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/check_docking/stored/django/admin.py
# Compiled at: 2015-02-08 00:14:31
__author__ = 'kylinfish@126.com'
__date__ = '2015/02/06'
from django.contrib import admin
from check_docking.stored.django.models import Interface, Method, DataItem

class DataItemInline(admin.StackedInline):
    u"""数据
    """
    model = DataItem


class MethodInline(admin.StackedInline):
    u"""方法
    """
    model = Method
    inlines = [DataItemInline]


class InterfaceAdmin(admin.ModelAdmin):
    u"""自定义ModelAdmin.
    """
    list_display = ('url_path', 'def_name', 'created_at', 'updated_at')
    ordering = ('-created_at', )
    list_filter = ('updated_at', )
    search_fields = ('url_path', 'def_name')
    inlines = [MethodInline]


class MethodAdmin(admin.ModelAdmin):
    u"""自定义ModelAdmin.
    """
    list_display = ('used_interface', 'name_method', 'created_at', 'updated_at')
    ordering = ('-created_at', )
    list_filter = ('updated_at', )
    search_fields = ('used_interface__url_path', 'used_interface__def_name')
    inlines = [DataItemInline]


class DataItemAdmin(admin.ModelAdmin):
    u"""自定义ModelAdmin.
    """
    list_display = ('used_method', 'data_name', 'data_type', 'data_must', 'data_value',
                    'created_at', 'updated_at')
    ordering = ('-created_at', )
    list_filter = ('updated_at', )
    search_fields = ('used_interface__url_path', 'used_interface__def_name')


admin.site.register(Method, MethodAdmin)
admin.site.register(DataItem, DataItemAdmin)
admin.site.register(Interface, InterfaceAdmin)