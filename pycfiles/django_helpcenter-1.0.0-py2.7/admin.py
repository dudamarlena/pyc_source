# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/admin.py
# Compiled at: 2016-09-30 00:56:02
from django.contrib import admin
from helpcenter import models

class ArticleAdmin(admin.ModelAdmin):
    """ Admin for the Article model """
    date_hierarchy = 'time_published'
    fieldsets = (
     (
      None,
      {'fields': ('category', 'title', 'body')}),
     (
      'Publishing Options',
      {'classes': ('collapse', ), 
         'fields': ('draft', 'time_published')}))
    list_display = ('title', 'category', 'time_published', 'time_edited', 'draft')
    search_fields = ('title', )


class CategoryAdmin(admin.ModelAdmin):
    """ Admin for the Category model """
    fieldsets = (
     (
      None,
      {'fields': ('parent', 'title')}),)
    list_display = ('title', 'parent')
    search_fields = ('title', )


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category, CategoryAdmin)