# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms_menu/admin.py
# Compiled at: 2014-11-14 09:29:30
from django.contrib import admin
from models import *
from tinycms.admin import register

class MenuItemAdmin(admin.ModelAdmin):
    list_display = [
     'page', 'language', 'title']


admin.site.register(MenuItem, MenuItemAdmin)

class MenuInline(admin.StackedInline):
    model = MenuItem
    extra = 1


register(MenuInline, 0)