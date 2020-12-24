# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/admin.py
# Compiled at: 2015-11-01 17:29:09
from django.contrib import admin
from models import User, Media, Comment

class AllFieldsReadOnly(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [ field.name for field in obj._meta.fields ]
        return []


class UserAdmin(AllFieldsReadOnly):

    def instagram_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.instagram_link, obj.username)

    instagram_link.allow_tags = True
    list_display = [
     'id', 'full_name', 'instagram_link']
    search_fields = ('username', 'full_name')
    exclude = ('followers', )


class MediaAdmin(AllFieldsReadOnly):

    def instagram_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.link, obj.link)

    instagram_link.allow_tags = True
    list_display = [
     'id', 'user', 'caption', 'created_time', 'instagram_link']
    search_fields = ('caption', )


class CommentAdmin(AllFieldsReadOnly):
    list_display = [
     'id', 'user', 'media', 'text', 'created_time']
    search_fields = ('text', )


class TagAdmin(AllFieldsReadOnly):
    list_display = [
     'id', 'name', 'media_count', 'created_time']
    search_fields = ('name', )


admin.site.register(User, UserAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Comment, CommentAdmin)