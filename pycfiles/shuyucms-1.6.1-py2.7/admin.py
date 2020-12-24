# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/generic/admin.py
# Compiled at: 2016-07-26 12:14:13
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin
from shuyucms.conf import settings
from shuyucms.generic.models import ThreadedComment, AssignedKeyword, Keyword

class ThreadedCommentAdmin(CommentsAdmin):
    """
    Admin class for comments.
    """
    list_display = ('id', 'user', 'submit_date', 'content_object', 'intro', 'is_removed',
                    'support_count', 'admin_link')
    list_display_links = ('user', 'intro')
    list_filter = [ f for f in CommentsAdmin.list_filter if f != b'site' ]
    fieldsets = (
     (
      None, {b'fields': ('user', 'comment', 'is_removed', 'support_count')}),)
    search_fields = [
     b'comment']

    def get_actions(self, request):
        actions = super(CommentsAdmin, self).get_actions(request)
        actions.pop(b'flag_comments')
        return actions

    def has_add_permission(self, request):
        return False


generic_comments = getattr(settings, b'COMMENTS_APP', b'') == b'shuyucms.generic'
if generic_comments:
    admin.site.register(ThreadedComment, ThreadedCommentAdmin)

def delnullkeywords(modeladmin, request, queryset):
    objs = AssignedKeyword.objects.all()
    for obj in objs:
        if not obj.content_object:
            obj.delete()


delnullkeywords.short_description = b'删除所有缺失的 已分配的关键词（请在半夜运行）'

class AssignedKeywordAdmin(admin.ModelAdmin):
    fieldsets = (
     (
      None, {b'fields': [b'keyword']}),)
    list_display = [b'id', b'keyword', b'content_object', b'content_type']
    raw_id_fields = [b'keyword']
    ordering = ('-id', )
    actions = [delnullkeywords]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(AssignedKeywordAdmin, self).get_actions(request)
        if b'delete_selected' in actions:
            del actions[b'delete_selected']
        return actions


admin.site.register(AssignedKeyword, AssignedKeywordAdmin)

class KeywordAdmin(admin.ModelAdmin):
    fieldsets = (
     (
      None, {b'fields': [b'title', b'parent', b'assigned_num']}),)
    list_display = [b'id', b'title', b'parent', b'assigned_num']
    raw_id_fields = ('parent', )
    search_fields = [b'^title']


admin.site.register(Keyword, KeywordAdmin)