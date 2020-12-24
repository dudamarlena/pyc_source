# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-users/facebook_users/admin.py
# Compiled at: 2015-03-06 07:15:54
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic
from facebook_api.admin import FacebookModelAdmin
from models import User

class UserAdmin(FacebookModelAdmin):
    list_display = ('name', 'first_name', 'last_name', 'gender')
    list_display_links = ('name', )
    list_filter = ('gender', )
    search_fields = ('name', )


if 'facebook_posts' in settings.INSTALLED_APPS:
    from facebook_posts.models import PostOwner, Comment

    class PostInline(generic.GenericTabularInline):
        model = PostOwner
        ct_field = 'owner_content_type'
        ct_fk_field = 'owner_id'
        fields = ('post', )
        readonly_fields = fields
        extra = False
        can_delete = False


    class CommentInline(generic.GenericTabularInline):
        model = Comment
        ct_field = 'author_content_type'
        ct_fk_field = 'author_id'
        fields = ('message', 'likes_count')
        readonly_fields = fields
        extra = False
        can_delete = False


    UserAdmin.inlines = [
     PostInline, CommentInline]
admin.site.register(User, UserAdmin)