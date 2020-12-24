# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flaviocaetano/github/pelican_admin/pelican_admin/admin/blog_post_admin.py
# Compiled at: 2012-12-10 07:06:07
__author__ = 'Flavio'
from pelican_admin.models.blog_post import BlogPost
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

class BlogPostAdmin(admin.ModelAdmin):
    fieldsets = (
     (
      None,
      {'fields': ('title', 'markup', 'lang', 'summary', 'text', 'date')}),
     (
      _('Extra Info'),
      {'classes': [
                   'collapse'], 
         'fields': ('slug', 'tags', 'category', 'author', 'status', 'file_path')}))
    list_display = ('title', 'markup', 'lang', 'status', 'date')
    ordering = ('-date', 'title')
    list_filter = ('category', 'status')
    search_fields = ('title', 'text', 'tags', 'category__name')
    date_hierarchy = 'date'

    def get_readonly_fields(self, request, obj=None):
        return ['file_path']


admin.site.register(BlogPost, BlogPostAdmin)