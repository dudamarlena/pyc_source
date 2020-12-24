# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-vkontakte-groups-statistic/vkontakte_groups_statistic/admin.py
# Compiled at: 2013-05-07 14:49:18
from django.contrib import admin
from vkontakte_api.admin import VkontakteModelAdmin
from vkontakte_groups.admin import Group, GroupAdmin as GroupAdminOriginal
from models import GroupStat

class GroupStatInline(admin.TabularInline):
    model = GroupStat
    fields = ('date', 'visitors', 'views', 'likes', 'comments', 'shares', 'new_members',
              'ex_members', 'members', 'ads_visitors', 'ads_members', 'males', 'females')
    readonly_fields = fields
    extra = 0
    can_delete = False


class GroupAdmin(GroupAdminOriginal):
    inlines = GroupAdminOriginal.inlines + [GroupStatInline]


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)