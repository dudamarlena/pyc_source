# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halit/pytr/pytrorg/src/sources/admin.py
# Compiled at: 2012-09-09 10:46:31
from django.contrib import admin
from sources.models import Categories, Sources, Types
from django import forms
from django.db import models

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    prepopulated_fields = {'slug': ('title', )}


class TypesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    prepopulated_fields = {'slug': ('title', )}


class SourcesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'created', 'edited')
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Sources, SourcesAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Types, TypesAdmin)