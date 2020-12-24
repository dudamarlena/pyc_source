# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wojciech/.pyenv/versions/3.7.3/lib/python3.7/site-packages/django_password_validators/password_history/admin.py
# Compiled at: 2016-03-01 06:07:03
# Size of source mod 2**32: 549 bytes
from django.contrib import admin
from .models import PasswordHistory, UserPasswordHistoryConfig

class UserPasswordHistoryConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'iterations')
    list_filter = ('date', )
    ordering = ('date', )


class PasswordHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_config', 'date')
    list_filter = ('date', )
    ordering = ('date', )


admin.site.register(UserPasswordHistoryConfig, UserPasswordHistoryConfigAdmin)
admin.site.register(PasswordHistory, PasswordHistoryAdmin)