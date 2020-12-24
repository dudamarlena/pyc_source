# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/photos/admin.py
# Compiled at: 2009-10-31 23:19:40
from django.contrib import admin
from photos.models import Image, Pool

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_slug', 'caption', 'date_added', 'is_public', 'member',
                    'safetylevel', 'tags')


class PoolAdmin(admin.ModelAdmin):
    list_display = ('photo', )


admin.site.register(Image, PhotoAdmin)
admin.site.register(Pool, PoolAdmin)