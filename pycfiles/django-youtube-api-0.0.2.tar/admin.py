# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/movister/env/src/django-youtube-api/youtube_api/admin.py
# Compiled at: 2015-09-09 16:36:14
from django.contrib import admin
from models import Video

class AllFieldsReadOnly(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [ field.name for field in obj._meta.fields ]
        return []


class VideoAdmin(AllFieldsReadOnly):
    pass


admin.site.register(Video, VideoAdmin)