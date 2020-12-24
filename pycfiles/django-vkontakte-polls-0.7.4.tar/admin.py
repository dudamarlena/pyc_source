# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-polls/vkontakte_polls/admin.py
# Compiled at: 2016-03-11 12:36:30
from django.contrib import admin
from django.utils.translation import ugettext as _
from vkontakte_api.admin import VkontakteModelAdmin
from models import Poll, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    can_delete = False
    fields = ('text', 'votes_count', 'rate')
    readonly_fields = fields


class PollAdmin(VkontakteModelAdmin):
    list_display = ('question', 'created', 'votes_count', 'post')
    list_display_links = ('question', )
    search_fields = ('question', )
    inlines = [
     AnswerInline]


admin.site.register(Poll, PollAdmin)