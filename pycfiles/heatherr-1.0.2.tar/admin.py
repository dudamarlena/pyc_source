# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/smn/heatherr/heatherr/groups/admin.py
# Compiled at: 2016-01-28 05:47:10
from django.contrib import admin
from heatherr.groups.models import Group, Person

class GroupModelAdmin(admin.ModelAdmin):
    pass


class PersonModeladmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupModelAdmin)
admin.site.register(Person, PersonModeladmin)