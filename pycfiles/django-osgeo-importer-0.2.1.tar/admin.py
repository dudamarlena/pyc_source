# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/admin.py
# Compiled at: 2016-12-22 15:59:44
from .models import UploadedData, UploadLayer, UploadFile
from django.contrib import admin

class UploadAdmin(admin.ModelAdmin):
    pass


class UploadedLayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'layer', 'feature_count', 'task_id')


class UploadedDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'state', 'size', 'complete')
    list_filter = ('user', 'state', 'complete')


admin.site.register(UploadLayer, UploadedLayerAdmin)
admin.site.register(UploadedData, UploadedDataAdmin)
admin.site.register(UploadFile, UploadAdmin)