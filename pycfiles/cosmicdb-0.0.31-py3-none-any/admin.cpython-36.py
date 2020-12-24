# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\david\Projects\cosmicdb\cosmicdb\admin.py
# Compiled at: 2018-06-24 08:39:58
# Size of source mod 2**32: 633 bytes
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from cosmicdb.models import UserSystemMessage, UserSystemNotification

class UserSystemMessageInlineAdmin(admin.TabularInline):
    model = UserSystemMessage


class UserSystemNotificationInlineAdmin(admin.TabularInline):
    model = UserSystemNotification


class UserProfileAdmin(UserAdmin):
    inlines = [
     UserSystemMessageInlineAdmin,
     UserSystemNotificationInlineAdmin]


user_model = get_user_model()
admin.site.register(user_model, UserProfileAdmin)