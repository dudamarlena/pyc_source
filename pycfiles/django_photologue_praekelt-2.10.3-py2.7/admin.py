# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/photologue/admin.py
# Compiled at: 2014-04-07 04:12:05
""" Newforms Admin configuration for Photologue

"""
from django.contrib import admin
from django.contrib.contenttypes import generic
from models import *

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'photo_count', 'is_public')
    list_filter = ['date_added', 'is_public']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'title_slug': ('title', )}
    filter_horizontal = ('photos', )


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'tags', 'view_count',
                    'admin_thumbnail')
    list_filter = ['date_added', 'is_public']
    search_fields = ['title', 'title_slug', 'caption']
    list_per_page = 10
    prepopulated_fields = {'title_slug': ('title', )}


class PhotoEffectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color', 'brightness', 'contrast', 'sharpness',
                    'filters', 'admin_sample')
    fieldsets = (
     (
      None,
      {'fields': ('name', 'description')}),
     (
      'Adjustments',
      {'fields': ('color', 'brightness', 'contrast', 'sharpness')}),
     (
      'Filters',
      {'fields': ('filters', )}),
     (
      'Reflection',
      {'fields': ('reflection_size', 'reflection_strength', 'background_color')}),
     (
      'Transpose',
      {'fields': ('transpose_method', )}))


class PhotoSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', 'crop', 'pre_cache', 'effect', 'increment_count')
    fieldsets = (
     (
      None,
      {'fields': ('name', 'width', 'height', 'quality')}),
     (
      'Options',
      {'fields': ('upscale', 'crop', 'pre_cache', 'increment_count')}),
     (
      'Enhancements',
      {'fields': ('effect', 'watermark')}))


class WatermarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'opacity', 'style')


class GalleryUploadAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False


class ImageOverrideInline(generic.GenericTabularInline):
    model = ImageOverride


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoEffect, PhotoEffectAdmin)
admin.site.register(PhotoSize, PhotoSizeAdmin)
admin.site.register(Watermark, WatermarkAdmin)