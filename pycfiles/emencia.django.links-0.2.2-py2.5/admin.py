# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emencia/django/links/admin.py
# Compiled at: 2010-01-14 11:17:33
"""Admin for emencia.django.links"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from emencia.django.links.models import Category
from emencia.django.links.models import Link

class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'language', 'visibility', 'site')
    date_hierarchy = 'creation'
    list_filter = ('visibility', 'site', 'creation')
    search_fields = ('title', 'description', 'url')
    fieldsets = ((None, {'fields': ('title', 'description', 'url')}),
     (
      _('Attributs'), {'fields': ('language', 'category')}),
     (
      _('Metadata'),
      {'fields': ('visibility', 'site', 'ordering', 'publication_start', 'publication_end')}))


admin.site.register(Link, LinkAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)