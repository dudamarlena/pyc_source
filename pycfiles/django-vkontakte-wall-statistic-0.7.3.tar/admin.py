# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-wall-statistic/vkontakte_wall_statistic/admin.py
# Compiled at: 2015-03-06 07:14:17
from django.contrib import admin
from vkontakte_wall.admin import Post, PostAdmin as PostAdminOriginal
from models import PostStatistic

class PostStatisticInline(admin.TabularInline):
    model = PostStatistic
    fields = ('date', 'reach', 'reach_subscribers', 'link_clicks', 'reach_males', 'reach_females',
              'reach_age_18', 'reach_age_18_21', 'reach_age_21_24', 'reach_age_24_27',
              'reach_age_27_30', 'reach_age_30_35', 'reach_age_35_45', 'reach_age_45',
              'reach_males_age_18', 'reach_males_age_18_21', 'reach_males_age_21_24',
              'reach_males_age_24_27', 'reach_males_age_27_30', 'reach_males_age_30_35',
              'reach_males_age_35_45', 'reach_males_age_45', 'reach_females_age_18',
              'reach_females_age_18_21', 'reach_females_age_21_24', 'reach_females_age_24_27',
              'reach_females_age_27_30', 'reach_females_age_30_35', 'reach_females_age_35_45',
              'reach_females_age_45')
    readonly_fields = fields
    extra = 0
    can_delete = False


class PostAdmin(PostAdminOriginal):
    inlines = PostAdminOriginal.inlines + [PostStatisticInline]


admin.site.unregister(Post)
admin.site.register(Post, PostAdmin)