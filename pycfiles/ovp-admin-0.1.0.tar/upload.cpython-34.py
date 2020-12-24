# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cidiomar/DEV/atados/gpa.main/api/django-ovp-admin/ovp_admin/modules/upload.py
# Compiled at: 2017-01-09 10:17:09
# Size of source mod 2**32: 614 bytes
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


admin.site.register(UploadedImage, UploadedImageAdmin)