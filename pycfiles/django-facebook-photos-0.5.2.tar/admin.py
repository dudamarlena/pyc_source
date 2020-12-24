# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-facebook-photos/facebook_photos/admin.py
# Compiled at: 2015-01-25 03:13:36
from django.contrib import admin
from django.core.urlresolvers import reverse
from facebook_api.admin import FacebookModelAdmin
from .models import Album, Photo

class PhotoInline(admin.TabularInline):

    def image(self, instance):
        return '<img src="%s" />' % (instance.picture,)

    image.short_description = 'photo'
    image.allow_tags = True
    model = Photo
    fields = ('name', 'place', 'created_time')
    readonly_fields = fields
    extra = False
    can_delete = False


class AlbumAdmin(FacebookModelAdmin):
    list_display = ('name', 'graph_id', 'photos_count', 'likes_count', 'comments_count',
                    'author', 'place', 'privacy', 'type', 'created_time', 'updated_time')
    list_display_links = ('name', )
    search_fields = ('name', 'description')
    inlines = [PhotoInline]


class PhotoAdmin(FacebookModelAdmin):

    def image_preview(self, obj):
        return '<a href="%s"><img src="%s" height="30" /></a>' % (obj.link, obj.picture)

    image_preview.short_description = 'Картинка'
    image_preview.allow_tags = True
    list_display = ('graph_id', 'image_preview', 'likes_count', 'comments_count', 'name',
                    'place', 'created_time')
    list_filter = ('album', )


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)