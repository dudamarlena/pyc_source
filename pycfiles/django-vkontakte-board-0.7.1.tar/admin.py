# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-board/vkontakte_board/admin.py
# Compiled at: 2015-02-19 12:23:23
from django.contrib import admin
from django.utils.translation import ugettext as _
from vkontakte_api.admin import VkontakteModelAdmin
from models import Topic, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    can_delete = False
    fields = ('author', 'text', 'date')
    readonly_fields = fields


class TopicAdmin(VkontakteModelAdmin):
    list_display = ('group', 'title', 'created', 'updated')
    list_display_links = ('title', )
    search_fields = ('text', )
    inlines = [
     CommentInline]


admin.site.register(Topic, TopicAdmin)