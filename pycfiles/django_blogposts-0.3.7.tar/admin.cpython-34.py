# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/admin.py
# Compiled at: 2018-08-06 04:08:22
# Size of source mod 2**32: 1094 bytes
from django.contrib import admin
from .models.blogpost import BlogPost
from .models.categories import Categories
from .models.tags import Tags
from django.conf import settings
__author__ = 'spi4ka'
post_exclude = []
if not getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
    post_exclude.append('category')
else:

    @admin.register(Categories)
    class CategoriesAdmin(admin.ModelAdmin):
        search_fields = ('name', 'slug', 'da')
        prepopulated_fields = {'slug': ('name', )}
        list_filter = ['is_moderated']


if not getattr(settings, 'BLOGPOSTS_USE_TAGS', True):
    post_exclude.append('tags')
else:

    @admin.register(Tags)
    class TagsAdmin(admin.ModelAdmin):
        search_fields = ('name', 'slug', 'da')
        prepopulated_fields = {'slug': ('name', )}
        list_filter = ['is_moderated']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    search_fields = ('header', 'meta_title', 'slug', 'da')
    prepopulated_fields = {'slug': ('header', )}
    list_filter = ['is_moderated']
    exclude = post_exclude