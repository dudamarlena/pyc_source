# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-vkontakte-groups-migration/vkontakte_groups_migration/admin.py
# Compiled at: 2014-04-05 04:06:31
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from vkontakte_api.admin import VkontakteModelAdmin
from vkontakte_groups.admin import Group, GroupAdmin as GroupAdminOriginal
from models import GroupMigration

class GroupMigrationInline(admin.TabularInline):
    model = GroupMigration
    fields = ('id', 'group', 'time', 'offset', 'hidden', 'members_count', 'members_entered_count',
              'members_left_count')
    readonly_fields = fields
    ordering = ('-time', )
    extra = 0
    can_delete = False

    def queryset(self, request):
        qs = super(GroupMigrationInline, self).queryset(request)
        return qs.light.exclude(time__isnull=True)


class GroupAdmin(GroupAdminOriginal):
    inlines = GroupAdminOriginal.inlines + [GroupMigrationInline]


class GroupMigrationAdmin(VkontakteModelAdmin):
    list_display = ('group', 'time')
    list_display_links = ('time', )


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMigration, GroupMigrationAdmin)