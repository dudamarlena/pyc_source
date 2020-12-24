# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-twitter-api/twitter_api/admin.py
# Compiled at: 2015-11-01 17:29:06
from django.contrib import admin
from models import Status, User

class TwitterModelAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [ field.name for field in obj._meta.fields ]
        return []


class StatusAdmin(TwitterModelAdmin):
    list_display = [
     'id', 'author', 'text']


class UserAdmin(TwitterModelAdmin):
    exclude = ('followers', )
    search_fields = ('name', 'screen_name')


admin.site.register(Status, StatusAdmin)
admin.site.register(User, UserAdmin)