# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gallery/admin.py
# Compiled at: 2010-07-19 06:54:12
from django.contrib import admin
from panya.admin import ModelBaseAdmin
from gallery.models import Gallery, GalleryImage, VideoEmbed, VideoFile

class GalleryImageAdmin(ModelBaseAdmin):
    list_display = ModelBaseAdmin.list_display + ('gallery', )
    list_filter = ModelBaseAdmin.list_filter + ('gallery', )


admin.site.register(Gallery, ModelBaseAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(VideoEmbed, ModelBaseAdmin)
admin.site.register(VideoFile, ModelBaseAdmin)