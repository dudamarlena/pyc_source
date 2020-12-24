# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms/admin.py
# Compiled at: 2014-11-14 09:25:00
from django.contrib import admin
from django.conf import settings
from mptt.admin import MPTTModelAdmin
from models import *

class ContentInline(admin.StackedInline):
    model = Content
    extra = 0


class PageAdmin(MPTTModelAdmin):
    inlines = [
     ContentInline]


admin.site.register(Page, PageAdmin)

class ContentAdmin(admin.ModelAdmin):
    list_display = [
     'page', 'value_name']


admin.site.register(Content, ContentAdmin)

def register(inlineClass, index=-1):
    if index == -1:
        PageAdmin.inlines.append(inlineClass)
    else:
        PageAdmin.inlines.insert(index, inlineClass)