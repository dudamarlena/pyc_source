# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pielgrzym/work/imaging/git/example_project/imaging/admin.py
# Compiled at: 2012-06-06 15:56:48
from django.contrib import admin
from imaging.models import *

class ImageAdmin(admin.ModelAdmin):
    exclude = [
     'ordering', 'content_type']
    list_display = ('name', 'title')


admin.site.register(Image, ImageAdmin)