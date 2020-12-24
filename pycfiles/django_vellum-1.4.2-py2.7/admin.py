# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/admin.py
# Compiled at: 2012-04-05 15:23:29
from django.contrib import admin
from vellum.models import *
from vellum import settings

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    display_fields = [
     'title', 'slug', 'author', 'markup', 'body', 'tease',
     'status', 'allow_comments', 'publish', 'categories',
     'tags']
    list_display = ('title', 'publish', 'status', 'visits')
    list_filter = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    if settings.BLOG_WMD:
        try:
            from vellum.forms import PostForm
        except ImportError:
            pass
        else:
            form = PostForm
            display_fields.remove('markup')

    fieldsets = (
     (None,
      {'fields': display_fields}),
     (
      'Rendered markup',
      {'classes': ('collapse', ), 
         'fields': ('body_rendered', 'tease_rendered')}))


admin.site.register(Post, PostAdmin)

class BlogRollAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'sort_order')
    list_editable = ('sort_order', )


admin.site.register(BlogRoll)