# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/news/admin.py
# Compiled at: 2014-03-27 09:47:06
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Category, Article
from .forms import ArticleAdminForm

class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    """
    list_display = ('title', 'slug', 'order')
    list_editable = ('order', )
    search_fields = ('title', )
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'slug', 'publish', 'publish_on')
    search_fields = ('title', )
    prepopulated_fields = {'slug': ('title', )}
    readonly_fields = ('created_on', 'updated_on')
    date_hierarchy = 'publish_on'
    fieldsets = (
     (
      _('Article'),
      {'fields': ('title', 'slug', 'category', 'content', 'image')}),
     (
      _('Publish'),
      {'fields': ('publish', 'publish_on')}),
     (
      _('Record Details'),
      {'fields': ('created_on', 'updated_on'), 
         'classes': ('collapse', )}))


admin.site.register(Article, ArticleAdmin)