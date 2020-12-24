# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/cmsplugin_phlog/admin.py
# Compiled at: 2013-06-26 16:38:22
from django.contrib import admin
from cmsplugin_phlog.models import OrderedGallery, PhotoOrdering

class PhotoInline(admin.TabularInline):
    model = OrderedGallery.photos.through
    template = 'admin/photologue/orderedgallery/inline_photos.html'
    fields = ('order', 'photo')
    ordering = ('order', )
    extra = 1


class OrderedGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'photo_count', 'is_public')
    list_filter = ['date_added', 'is_public']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'title_slug': ('title', )}
    filter_horizontal = ('photos', )
    inlines = [PhotoInline]


admin.site.register(OrderedGallery, OrderedGalleryAdmin)