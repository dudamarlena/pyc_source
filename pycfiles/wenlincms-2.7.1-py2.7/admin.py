# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/generic/admin.py
# Compiled at: 2016-05-25 13:02:46
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.comments.admin import CommentsAdmin
from wenlincms.conf import settings
from wenlincms.generic.models import ThreadedComment, Keyword
from wlapps.utils.common_a import synckeywordsfreq

class ThreadedCommentAdmin(CommentsAdmin):
    """
    Admin class for comments.
    """
    list_display = ('id', 'user', 'submit_date', 'content_object', 'intro', 'support_count',
                    'admin_link')
    list_display_links = ('user', 'intro')
    list_filter = [ f for f in CommentsAdmin.list_filter if f != b'site' ]
    fieldsets = ((None, {b'fields': ('user', 'comment', 'submit_date', 'ip_address', 'support_count')}),)
    search_fields = [b'comment']
    readonly_fields = [b'user', b'submit_date', b'ip_address', b'support_count']

    def get_actions(self, request):
        actions = super(CommentsAdmin, self).get_actions(request)
        actions.pop(b'flag_comments')
        actions.pop(b'approve_comments')
        actions.pop(b'remove_comments')
        return actions

    def has_add_permission(self, request):
        return False


generic_comments = getattr(settings, b'COMMENTS_APP', b'') == b'wenlincms.generic'
if generic_comments:
    admin.site.register(ThreadedComment, ThreadedCommentAdmin)

class AssignedKeywordAdmin(admin.ModelAdmin):
    fieldsets = (
     (
      None, {b'fields': [b'keyword']}),)
    list_display = [b'id', b'keyword', b'content_object', b'content_type']

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(AssignedKeywordAdmin, self).get_actions(request)
        if b'delete_selected' in actions:
            del actions[b'delete_selected']
        return actions


class KeywordAdmin(admin.ModelAdmin):
    fieldsets = (
     (
      None, {b'fields': [b'title', b'parent', b'assigned_num']}),)
    list_display = [b'id', b'title', b'parent', b'assigned_num']
    raw_id_fields = ('parent', )
    search_fields = [b'=^title']
    readonly_fields = [b'assigned_num']
    actions = [synckeywordsfreq]


admin.site.register(Keyword, KeywordAdmin)