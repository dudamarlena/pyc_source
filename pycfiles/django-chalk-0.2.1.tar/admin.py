# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/virtualenvs/kd/src/chalk/chalk/admin.py
# Compiled at: 2013-08-26 13:55:54
from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'publication_date')
    prepopulated_fields = {'slug': ('title', )}
    fieldsets = (
     (
      None,
      {'fields': ('author', 'title', 'content', 'excerpt', 'published', 'publication_date')}),
     (
      'Advanced',
      {'classes': ('collapse', ), 
         'fields': ('protect_html', 'content_html', 'excerpt_html', 'slug', 'meta_description')}))


admin.site.register(Article, ArticleAdmin)