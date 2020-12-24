# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-uploads/ovp_uploads/admin.py
# Compiled at: 2017-06-13 10:26:45
# Size of source mod 2**32: 1304 bytes
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from ovp_uploads.models import UploadedImage

class UploadedImageAdmin(admin.ModelAdmin):
    fields = [
     'id', 'image', 'image_small', 'image_medium', 'image_large']
    list_display = [
     'id', 'image', 'user']
    list_filter = []
    list_editable = []
    search_fields = [
     'id', 'user__name', 'user__email']
    readonly_fields = [
     'id', 'image_small', 'image_medium', 'image_large']
    raw_id_fields = [
     'user']


class ImageGalery(UploadedImage):

    class Meta:
        proxy = True
        verbose_name = _('image gallery')
        verbose_name_plural = _('image galleries')


class ImageGaleryAdmin(admin.ModelAdmin):
    fields = [
     'id', 'name', 'category', 'image', 'image_small', 'image_medium', 'image_large']
    list_display = [
     'id', 'name', 'category', 'image']
    list_filter = [
     'category']
    list_editable = []
    search_fields = [
     'id', 'name']
    readonly_fields = [
     'id', 'image_small', 'image_medium', 'image_large']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category__isnull=False)


admin.site.register(UploadedImage, UploadedImageAdmin)
admin.site.register(ImageGalery, ImageGaleryAdmin)